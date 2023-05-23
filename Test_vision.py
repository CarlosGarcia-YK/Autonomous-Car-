import cv2
import urllib.request
import numpy as np
import time
import traitlets
import os
import shutil 

STEERING_OFFSET = 0.035
THROTTLE_GAIN = 0.7

CAMERA_WIDTH = 448
CAMERA_HEIGHT = 336

FPS = 10
SHOW_CAMERA_PREVIEW = False

DATASETS_DIR = "/home/greg/datasets/"
TMP_DATASET_DIR = DATASETS_DIR + "tmp/"
ANNOTATIONS_FILE = "annotations.csv"
TMP_ANNOTATIONS = TMP_DATASET_DIR + ANNOTATIONS_FILE

DATASET_MODE = "training"
DATASET_NAME = "3"
MAIN_DATASET_DIR = DATASETS_DIR + DATASET_NAME + "_" + DATASET_MODE + "/"
MAIN_ANNOTATIONS = MAIN_DATASET_DIR + ANNOTATIONS_FILE

def reset_temp_dataset_dir():
    if not os.path.exists(TMP_DATASET_DIR):
        os.makedirs(TMP_DATASET_DIR)
    else:
        shutil.rmtree(TMP_DATASET_DIR)
        os.makedirs(TMP_DATASET_DIR)

reset_temp_dataset_dir()

if not os.path.exists(MAIN_DATASET_DIR):
    os.makedirs(MAIN_DATASET_DIR)


def start_recording():
    reset_temp_dataset_dir()
    
def save_recording():


    for file in os.listdir(TMP_DATASET_DIR):
        if file.endswith('.csv'):
            if os.path.exists(MAIN_ANNOTATIONS) and os.stat(MAIN_ANNOTATIONS).st_size > 0:
                with open(MAIN_ANNOTATIONS, 'a') as main:
                    with open(TMP_ANNOTATIONS) as tmp:
                        for line in tmp:
                            main.write(line)
                        tmp.close()
                    main.close()
                continue
        shutil.move(TMP_DATASET_DIR+file, MAIN_DATASET_DIR+file)
    
    reset_temp_dataset_dir()
def clamp(value, val_min=-1.0, val_max=1.0):
    return min(val_max, max(val_min, value))

def is_valid_press(x):
    return x['name'] == 'pressed' and x['new']

import cv2
import time

# Crear objeto para acceder a la cámara de la laptop
camera = cv2.VideoCapture(0)  # El número 0 indica la primera cámara disponible

# Definir dimensiones de la imagen y velocidad de captura
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30

# Configurar dimensiones de captura de la cámara
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
camera.set(cv2.CAP_PROP_FPS, FPS)

def save_annotated_camera_frame(frame):
    timestamp = str(int(time.time() * 1000))

    def save_camera_frame():
        cv2.imwrite(TMP_DATASET_DIR + timestamp + ".jpg", frame)

    def save_annotation():
        with open(TMP_ANNOTATIONS, 'a') as f:
            f.write(timestamp + ", " + str(round(car.steering, 2)) + ", " + str(round(car.throttle, 2)) + "\n")
            f.close()

    save_camera_frame()
    save_annotation()

    encoded_image = cv2.imencode('.jpg', frame)[1]
    return bytes(encoded_image)

while True:
    ret, frame = camera.read()  # Leer un cuadro de la cámara

    # Realizar operaciones adicionales en el cuadro, si es necesario

    annotated_frame = save_annotated_camera_frame(frame)

    # Mostrar o procesar el cuadro anotado, según sea necesario

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
camera.release()
cv2.destroyAllWindows()
