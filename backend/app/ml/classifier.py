import os
import numpy as np
from typing import Dict
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Ruta base del proyecto desde classifier.py (estás en backend/app/ml/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

# Rutas a los modelos entrenados
GARBAGE_MODEL_PATH = os.path.join(BASE_DIR, "ml-model", "model", "garbage_classifier.keras")
FOOD_MODEL_PATH = os.path.join(BASE_DIR, "ml-model", "model", "organic_classifier.keras")

# Etiquetas
garbage_labels = ["inorganico", "organico", "reciclable"]
food_labels = ["organico"]

# Carga de modelos
garbage_model = load_model(GARBAGE_MODEL_PATH)
food_model = load_model(FOOD_MODEL_PATH)

def predict_image_class(img_path: str, mode: str = "garbage") -> Dict:
    """
    Predice la clase de una imagen usando el modelo de residuos o de comida.
    Retorna el label y el porcentaje de confianza.
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if mode == "garbage":
        preds = garbage_model.predict(img_array)
        label_idx = np.argmax(preds)
        return {
            "label": garbage_labels[label_idx],
            "confidence": round(float(preds[0][label_idx]) * 100, 2)
        }

    elif mode == "food":
        preds = food_model.predict(img_array)

        # Si es modelo binario con una sola clase ("organico")
        if preds.shape[1] == 1:  # salida (None, 1)
            prob = float(preds[0][0]) * 100
            return {
                "label": "organico" if prob > 80 else "desconocido",
                "confidence": round(prob, 2)
            }

        # Si algún día agregas más clases de comida
        label_idx = np.argmax(preds)
        return {
            "label": food_labels[label_idx],
            "confidence": round(float(preds[0][label_idx]) * 100, 2)
        }

    return {"label": "desconocido", "confidence": 0.0}