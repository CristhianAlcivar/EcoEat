import os.path
import argparse
import json
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import sys
import time

parser = argparse.ArgumentParser(description='')
parser.add_argument('--dataset_path', required=False, default='./data/annotations.json', help='Path to annotations')
args = parser.parse_args()

dataset_dir = os.path.dirname(args.dataset_path)

print('Note. If for any reason the connection is broken. Just call me again and I will start where I left.')

# Load annotations
with open(args.dataset_path, 'r') as f:
    annotations = json.load(f)

nr_images = len(annotations['images'])

# Abrir archivo de log de errores
error_log_path = os.path.join(dataset_dir, "download_errors.txt")
error_log = open(error_log_path, "a", encoding="utf-8")

for i in range(nr_images):
    image = annotations['images'][i]
    file_name = image['file_name']
    url_original = image['flickr_url']
    file_path = os.path.join(dataset_dir, file_name)

    # Create subdir if necessary
    subdir = os.path.dirname(file_path)
    if not os.path.isdir(subdir):
        os.makedirs(subdir)

    if not os.path.isfile(file_path):
        try:
            response = requests.get(url_original, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            if img._getexif():
                img.save(file_path, exif=img.info.get("exif"))
            else:
                img.save(file_path)
        except requests.exceptions.RequestException as req_err:
            msg = f"[NETWORK ERROR] {url_original}: {req_err}"
            print(f"\n{msg}")
            error_log.write(msg + "\n")
            time.sleep(2)
            continue
        except UnidentifiedImageError as img_err:
            msg = f"[IMAGE ERROR] {url_original}: {img_err}"
            print(f"\n{msg}")
            error_log.write(msg + "\n")
            time.sleep(2)
            continue
        except Exception as e:
            msg = f"[OTHER ERROR] {url_original}: {e}"
            print(f"\n{msg}")
            error_log.write(msg + "\n")
            time.sleep(2)
            continue

    # Mostrar barra de progreso
    bar_size = 30
    x = int(bar_size * (i + 1) / nr_images)
    sys.stdout.write("%s[%s%s] - %i/%i\r" % ('Loading: ', "=" * x, "." * (bar_size - x), i + 1, nr_images))
    sys.stdout.flush()

    # Pausa corta entre imágenes
    time.sleep(0.1)

    # Cada 250 imágenes, esperar 60 segundos
    if (i + 1) % 250 == 0:
        print(f"\nEsperando 60 segundos para evitar saturar el servidor... ({i + 1}/{nr_images})")
        time.sleep(60)

error_log.close()
sys.stdout.write('Finished\n')
