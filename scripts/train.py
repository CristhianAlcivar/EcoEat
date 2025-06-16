import os
import pandas as pd
import numpy as np
import tensorflow as tf
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# ========= CONFIGURACIÓN =========
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20

CSV_PATH = 'data/processed/annotations.csv'
IMAGES_DIR = 'data/processed/images'
MODEL_DIR = 'models/taco_model'
MODEL_OUTPUT_PATH = os.path.join(MODEL_DIR, 'taco_model.keras')
TFLITE_OUTPUT_PATH = os.path.join(MODEL_DIR, 'taco_model.tflite')

# ========= CARGAR CSV =========
df = pd.read_csv(CSV_PATH)

# ========= ANALIZAR DATOS =========
print("\n🔍 Imágenes por clase:")
print(df['class'].value_counts())
print(f"\nTotal de imágenes: {len(df)}")
print(f"Total de clases: {df['class'].nunique()}")

# Opcional: visualizar algunas imágenes por clase
def show_examples(df, classes, images_dir, n=3):
    for c in classes:
        imgs = df[df['class'] == c]['filename'].values[:n]
        plt.figure(figsize=(n*2, 2))
        plt.suptitle(c)
        for i, fname in enumerate(imgs):
            img = cv2.imread(os.path.join(images_dir, fname))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.subplot(1, n, i+1)
            plt.imshow(img)
            plt.axis('off')
        plt.show()

# Muestra las 3 clases más frecuentes
top_classes = df['class'].value_counts().head(3).index
show_examples(df, top_classes, IMAGES_DIR, n=3)

# ========= ELIMINAR CLASES CON <2 IMÁGENES =========
counts = df["class"].value_counts()
classes_to_keep = counts[counts >= 2].index
df = df[df["class"].isin(classes_to_keep)]
classes = sorted(df["class"].unique())
class_to_index = {cls: i for i, cls in enumerate(classes)}
df["label"] = df["class"].map(class_to_index)

print("\nClases finales tras filtro (<2 imgs):", len(classes))

# ========= CARGAR Y PROCESAR IMÁGENES =========
X, y = [], []
for _, row in df.iterrows():
    img_path = os.path.join(IMAGES_DIR, row["filename"])
    label = row["label"]
    if not os.path.exists(img_path): continue
    try:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        X.append(img)
        y.append(label)
    except Exception: continue

X = np.array(X, dtype=np.float32)
y = np.array(y, dtype=np.int32)
if len(X) == 0: raise RuntimeError("No se cargaron imágenes.")

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

train_ds = tf.data.Dataset.from_tensor_slices((X_train, y_train)).shuffle(1000).batch(BATCH_SIZE)
val_ds = tf.data.Dataset.from_tensor_slices((X_val, y_val)).batch(BATCH_SIZE)

# ========= MODELO (sin augmentation para depurar) =========
num_classes = len(classes)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False, weights='imagenet'
)
base_model.trainable = False

model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ========= ENTRENAMIENTO =========
history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)

# ========= EVALUACIÓN =========
val_loss, val_acc = model.evaluate(val_ds)
print(f"\n🎯 Precisión final en validación: {val_acc*100:.2f}%")

# ========= MATRIZ DE CONFUSIÓN Y REPORTE =========
y_pred = []
y_true = []
for imgs, labels in val_ds:
    preds = model.predict(imgs)
    y_pred.extend(np.argmax(preds, axis=1))
    y_true.extend(labels.numpy())

# CLASES: asegúrate de que el mapeo sea correcto
num_classes = len(classes)
print("\nReporte de clasificación:")
print(classification_report(
    y_true, y_pred,
    labels=list(range(num_classes)),
    target_names=classes,
    zero_division=0
))

cm = confusion_matrix(y_true, y_pred, labels=list(range(num_classes)))
plt.figure(figsize=(12, 8))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=classes, yticklabels=classes, cmap="Blues")
plt.xlabel("Predicho")
plt.ylabel("Real")
plt.title("Matriz de confusión")
plt.tight_layout()
plt.show()

# ========= GUARDAR MODELO .keras =========
os.makedirs(MODEL_DIR, exist_ok=True)
model.save(MODEL_OUTPUT_PATH)
print(f"\n✅ Modelo guardado en: {MODEL_OUTPUT_PATH}")

# ========= GUARDAR MAPEO CLASES =========
index_to_class = {i: cls for cls, i in class_to_index.items()}
with open(os.path.join(MODEL_DIR, "index_to_class.json"), "w") as f:
    import json
    json.dump(index_to_class, f, indent=2)

# ========= EXPORTAR TFLITE =========
print("\n🔄 Exportando a TensorFlow Lite optimizado...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open(TFLITE_OUTPUT_PATH, 'wb') as f:
    f.write(tflite_model)
print(f"✅ Modelo TFLite guardado en: {TFLITE_OUTPUT_PATH}")
