import os
import shutil

# Ruta donde descomprimiste el dataset
SOURCE_PATH = "../garbage_classification"


# Tu estructura de destino
TARGET_PATH = "datasets"

# Mapeo de clases en Kaggle -> EcoEat
CLASS_MAP = {
    "cardboard": "reciclable",
    "metal": "reciclable",
    "paper": "reciclable",
    "plastic": "reciclable",
    "trash": "inorganico",

    # Añadir tipos de vidrio:
    "brown-glass": "reciclable",
    "green-glass": "reciclable",
    "white-glass": "reciclable"
}

def organizar_dataset():
    for origen, destino in CLASS_MAP.items():
        source_dir = os.path.join(SOURCE_PATH, origen)
        target_dir = os.path.join(TARGET_PATH, destino)
        os.makedirs(target_dir, exist_ok=True)

        for filename in os.listdir(source_dir):
            src_file = os.path.join(source_dir, filename)
            dst_file = os.path.join(target_dir, filename)
            shutil.copy(src_file, dst_file)

    print("✅ Dataset reorganizado con éxito.")

if __name__ == "__main__":
    organizar_dataset()
