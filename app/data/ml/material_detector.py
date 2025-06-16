import json
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

class MaterialDetector:
    def __init__(self, model_path: str, labels_path: str = "data/labels.json"):
        self.model = load_model(model_path)

        # Cargar etiquetas y clasificación desde labels.json
        with open(labels_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.renovables = set(data["renovables"])
            self.no_renovables = set(data["no_renovables"])
            self.labels = list(self.renovables.union(self.no_renovables))

    def predict(self, image_path: str) -> dict:
        img = Image.open(image_path).resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
        predictions = self.model.predict(img_array)[0]
        return {
            self.labels[i]: float(predictions[i]) for i in range(len(self.labels))
        }

    def contar_tipo_materiales(self, predicciones: dict) -> tuple[int, int]:
        renovables = sum(1 for m in predicciones if m in self.renovables)
        no_renovables = sum(1 for m in predicciones if m in self.no_renovables)
        return renovables, no_renovables
