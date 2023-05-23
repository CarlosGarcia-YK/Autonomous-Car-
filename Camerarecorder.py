import cv2
import urllib.request
import numpy as np
import time
import os

# Crear la carpeta 'images' si no existe
if not os.path.exists('images'):
    os.makedirs('images')

# Abrir el archivo de video
video = cv2.VideoWriter('test2.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (320, 240))

def save_image(img):
    # Guardar la imagen en la carpeta 'images'
    filename = f"image_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(os.path.join('images', filename), img)

# Capturar frames
for i in range(60000):  # Detener después de 60000 frames
    try:
        # Capturar el frame de la URL
        url = "http://192.168.128.91/cam-hi.jpg"
        img_resp = urllib.request.urlopen(url)
        img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = cv2.flip(img, 0)

        # Agregar el frame al video
        video.write(img)

        # Mostrar el frame en una ventana
        cv2.imshow('frame', img)

        # Guardar la imagen
        save_image(img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error: {str(e)}")

# Liberar el video
video.release()
cv2.destroyAllWindows()
