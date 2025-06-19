## Comandos para proyecto TACO + YOLOv5
Este documento resume todos los comandos necesarios para ejecutar el proyecto desde cero hasta la inferencia final.

## 1. Clonar el dataset TACO

git clone https://github.com/pedropro/TACO.git
cd TACO

## 2. Clonar YOLOv5

git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt

## 3. Descargar imagenes desde Flickr

python scripts/download_images.py

## 4. Generar archivo de etiquetas labels.json

python scripts/generate_labels_json.py

## 5. Procesar dataset recortando objetos

python scripts/prepare_dataset.py

## 6. Convertir de formato COCO a YOLOv5

python scripts/convert_to_yolo.py

## 7. Verificar y editar datasets/taco_yolo/taco.yaml si es necesario para la ruta donde esta alojadas las carpetas train y val

train: C:/Users/DANIEL/Desktop/Proyectos/TACO/datasets/taco_yolo/images/train
val: C:/Users/DANIEL/Desktop/Proyectos/TACO/datasets/taco_yolo/images/val

nc: 60  # Número de clases (ajustar si usas menos)
names:
  - Aluminium foil
  - Battery
  - Bottle
  - Bubble wrap

## 8. Entrenar modelo YOLOv5

python scripts/train_yolo.py

Configurar en train_yolo.py de acuerdo a los recursos de la maquina:

img_size = 640 
batch_size = 8
epochs = 100
weights = 'yolov5s.pt'

## 9. Realizar inferencia

python scripts/predict_yolo.py

modificar la imagen de prueba cambiando esta linea:

IMAGE_PATH = 'data/images/prueba.jpg'

## Resultado de prediccion (ejemplo de consola)

Prediccion:
- Categoria: Bottle
- Material: Plastic
- Reciclable: Si
- Valor estimado: $0.10
- Confianza: 85.67%

## Ejecutar proyecto
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload