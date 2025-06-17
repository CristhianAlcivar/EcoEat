import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
model_path = os.path.join(BASE_DIR, "ml-model", "model", "garbage_classifier.keras")

print("Ruta generada:", model_path)
print("¿Existe el archivo?", os.path.exists(model_path))
