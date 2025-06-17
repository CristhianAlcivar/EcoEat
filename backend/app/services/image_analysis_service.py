from typing import Dict
from app.ml.classifier import predict_image_class

MATERIAL_COSTS = {
    "inorganico": 0.05,
    "organico": 0.00,
    "reciclable": 0.10
}

MATERIAL_DESCRIPTIONS = {
    "inorganico": "vaso o plástico no reciclable",
    "reciclable": "botella, cartón o papel",
    "organico": "comida (carne, vegetales, etc)"
}

CLASS_CORRECTIONS = {
    "organico": "orgánico",
    "inorganico": "inorgánico",
    "reciclable": "reciclable",
    "mixto": "mixto",
    "desconocido": "desconocido"
}

def classify_materials_from_image(image_path: str) -> Dict:
    result = {
        "classification": "desconocido",
        "description": "desconocido",
        "estimated_cost": 0.0,
        "materials": [],
        "confidence_score": 0.0
    }

    detected_classes = []
    materials = []
    total_cost = 0.0
    confidences = []

    # Predicción con modelo de residuos
    garbage = predict_image_class(image_path, mode="garbage")
    if garbage["label"] in MATERIAL_COSTS:
        detected_classes.append(garbage["label"])
        materials.append(MATERIAL_DESCRIPTIONS[garbage["label"]])
        total_cost += MATERIAL_COSTS[garbage["label"]]
        confidences.append(garbage["confidence"])

    # Predicción con modelo de alimentos
    food = predict_image_class(image_path, mode="food")
    if food["label"] == "organico" and food["label"] not in detected_classes:
        detected_classes.append(food["label"])
        materials.append(MATERIAL_DESCRIPTIONS[food["label"]])
        total_cost += MATERIAL_COSTS[food["label"]]
        confidences.append(food["confidence"])

    # Armar resultado final
    if detected_classes:
        result["classification"] = CLASS_CORRECTIONS.get(
            "mixto" if len(detected_classes) > 1 else detected_classes[0],
            "desconocido"
        )
        result["description"] = ", ".join(materials)
        result["estimated_cost"] = round(total_cost, 2)
        result["materials"] = materials
        result["confidence_score"] = round(sum(confidences) / len(confidences), 2) if confidences else 0.0

    return result
