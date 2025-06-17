import os
import shutil
import random

# Ruta donde descomprimiste el dataset food-101
SOURCE_PATH = "../food-101"  # ajusta si está en otro lugar

# Ruta de destino para organizar como organico/
TARGET_PATH = "datasets_food"

# Selección de clases representativas
SELECTED_CLASSES = [
    "Meat", "Noodles-Pasta", "Rice", "Soup", "Vegetable-Fruit",
    "Seafood", "Bread", "Dairy product", "Dessert", "Egg"
]

# Cuántas imágenes copiar por clase
IMAGES_PER_CLASS = 500

def organizar_food_dataset():
    for food_class in SELECTED_CLASSES:
        source_dir = os.path.join(SOURCE_PATH, food_class)
        target_dir = os.path.join(TARGET_PATH, "organico", food_class)
        os.makedirs(target_dir, exist_ok=True)

        if not os.path.exists(source_dir):
            print(f"❌ No se encontró la carpeta: {source_dir}")
            continue

        all_images = os.listdir(source_dir)
        selected = random.sample(all_images, min(IMAGES_PER_CLASS, len(all_images)))

        for file in selected:
            src_file = os.path.join(source_dir, file)
            dst_file = os.path.join(target_dir, file)
            shutil.copy(src_file, dst_file)

        print(f"✅ {food_class}: {len(selected)} imágenes copiadas.")

    print("\n🎉 Dataset food reorganizado correctamente.")

if __name__ == "__main__":
    organizar_food_dataset()
