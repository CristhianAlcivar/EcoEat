import os
import json
import numpy as np
import tensorflow as tf
import cv2

# ========== CONFIGURACIÓN ==========
IMG_SIZE = 224
MODEL_PATH = 'models/taco_model/taco_model.keras'
LABELS_PATH = 'app/data/labels.json'

# ========== CARGAR MODELO ==========
model = tf.keras.models.load_model(MODEL_PATH)

# ========== CARGAR LABELS (lista o dict) ==========
with open(LABELS_PATH, 'r') as f:
    labels_data = json.load(f)

index_to_class = {}
class_info = {}

if isinstance(labels_data, list):
    for i, label in enumerate(labels_data):
        material = label['material']
        index_to_class[i] = material
        class_info[material] = {
            'class_name': material,
            'material': material,
            'recyclable': label['recyclable'],
            'value': label['value']
        }
elif isinstance(labels_data, dict):
    for i, (key, value) in enumerate(labels_data.items()):
        material = value['material']
        index_to_class[i] = material
        class_info[material] = {
            'class_name': key,
            'material': material,
            'recyclable': value['recyclable'],
            'value': value['value']
        }

# ========== FUNCIÓN DE PREDICCIÓN ==========
def predict_image(image_path):
    if not os.path.exists(image_path):
        return f"Imagen no encontrada: {image_path}"

    img = cv2.imread(image_path)
    if img is None:
        return f"No se pudo abrir la imagen: {image_path}"
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)[0]
    predicted_index = np.argmax(predictions)
    confidence = predictions[predicted_index]

    material = index_to_class[predicted_index]
    info = class_info[material]

    # Devuelve el resultado como string (ideal para WhatsApp)
    result = (
        f"Predicción de material:\n"
        f"🔹 Categoría: {info['class_name']}\n"
        f"🔹 Material: {info['material']}\n"
        f"🔹 Reciclable: {'Sí' if info['recyclable'] else 'No'}\n"
        f"🔹 Valor estimado: ${info['value']:.2f}\n"
        f"🔹 Confianza: {confidence*100:.2f}%"
    )
    return result

# ========== USO DESDE TERMINAL ==========
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python scripts/predict.py <ruta_imagen>")
    else:
        print(predict_image(sys.argv[1]))
