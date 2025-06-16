import json
from collections import defaultdict
import os

# Ruta al archivo original de anotaciones
ANNOTATIONS_PATH = os.path.join("data", "annotations.json")
OUTPUT_PATH = os.path.join("data", "labels.json")

# Puedes personalizar materiales, reciclabilidad y valor si sabes qué clases representan qué materiales
DEFAULT_CLASS_INFO = {
    "plastic": {"recyclable": True, "value": 0.01},
    "metal": {"recyclable": True, "value": 0.05},
    "glass": {"recyclable": True, "value": 0.10},
    "paper": {"recyclable": True, "value": 0.02},
    "organic": {"recyclable": False, "value": 0.00},
    "hazardous": {"recyclable": False, "value": 0.00},
    "other": {"recyclable": False, "value": 0.00}
}

def guess_material(name: str) -> str:
    """Aproximar el material del objeto a partir de su nombre (puedes personalizarlo más adelante)."""
    name = name.lower()
    if "plastic" in name or "bag" in name or "pet" in name:
        return "plastic"
    if "glass" in name:
        return "glass"
    if "can" in name or "metal" in name or "foil" in name:
        return "metal"
    if "paper" in name or "cardboard" in name:
        return "paper"
    if "food" in name or "organic" in name:
        return "organic"
    if "battery" in name or "hazard" in name:
        return "hazardous"
    return "other"

def generate_labels():
    with open(ANNOTATIONS_PATH, "r") as f:
        annotations = json.load(f)

    categories = annotations.get("categories", [])
    labels = {}

    for category in categories:
        class_name = category["name"]
        material = guess_material(class_name)
        info = DEFAULT_CLASS_INFO[material]
        labels[class_name] = {
            "material": material,
            "recyclable": info["recyclable"],
            "value": info["value"]
        }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(labels, f, indent=4)

    print(f"labels.json generado con {len(labels)} clases en {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_labels()