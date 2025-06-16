import os
import json
import shutil
from PIL import Image
from tqdm import tqdm

# Rutas
ANNOTATIONS_FILE = os.path.join("data", "annotations.json")
LABELS_FILE = os.path.join("data", "labels.json")
IMAGES_DIR = os.path.join("data", "images")  # Asegúrate de tener aquí las imágenes originales
OUTPUT_DIR = os.path.join("data", "processed")  # Aquí guardaremos los recortes

# Crear carpetas de salida
IMAGE_OUT_DIR = os.path.join(OUTPUT_DIR, "images")
ANNOTATION_OUT_PATH = os.path.join(OUTPUT_DIR, "annotations.csv")

os.makedirs(IMAGE_OUT_DIR, exist_ok=True)

# Cargar datos
with open(ANNOTATIONS_FILE) as f:
    annotations_data = json.load(f)

with open(LABELS_FILE) as f:
    labels_data = json.load(f)

# Crear mapeos
categories = {cat["id"]: cat["name"] for cat in annotations_data["categories"]}
images_info = {img["id"]: img for img in annotations_data["images"]}

# Procesar anotaciones
data = []
counter = 0

for ann in tqdm(annotations_data["annotations"], desc="Procesando anotaciones"):
    image_id = ann["image_id"]
    category_id = ann["category_id"]
    bbox = ann["bbox"]  # [x, y, width, height]

    class_name = categories[category_id]
    image_info = images_info[image_id]
    image_path = os.path.join(IMAGES_DIR, image_info["file_name"])

    if not os.path.exists(image_path):
        continue  # Saltar si falta la imagen

    try:
        with Image.open(image_path) as img:
            x, y, w, h = map(int, bbox)
            cropped = img.crop((x, y, x + w, y + h))

            # Guardar imagen recortada
            out_filename = f"{counter}_{class_name.replace(' ', '_')}.jpg"
            out_path = os.path.join(IMAGE_OUT_DIR, out_filename)
            cropped.save(out_path)

            # Obtener reciclabilidad y valor
            recyclable = labels_data[class_name]["recyclable"]
            value = labels_data[class_name]["value"]
            material = labels_data[class_name]["material"]

            # Agregar a la lista
            data.append(f"{out_filename},{class_name},{material},{recyclable},{value}")
            counter += 1
    except Exception as e:
        print(f"Error con imagen {image_path}: {e}")
        continue

# Guardar CSV
with open(ANNOTATION_OUT_PATH, "w") as f:
    f.write("filename,class,material,recyclable,value\n")
    for row in data:
        f.write(row + "\n")

print(f"\n✅ Dataset procesado: {counter} objetos guardados en {IMAGE_OUT_DIR}")
print(f"📄 Anotaciones en: {ANNOTATION_OUT_PATH}")
