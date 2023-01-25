from tkinter import *
from PIL import Image, ImageTk
import os
import numpy as np
import cv2
import datetime

recording = False

class DataRecorder:
    def _init_(self):
        pass
    def save_to_file(self, file_path, input_text):
        with open(file_path, "a") as file:
            file.write(f"{input_text}\n")


def save_text():
    input_text = text_input.get()
    recorder.save_to_file(file_path, input_text)

def record_keyboard(event):
    input_text = event.char
    recorder.save_to_file(file_path, input_text)


recorder = DataRecorder()
file_path = "data.txt"

def iniciarfunciones():
    global cameraObject, frame_count, fps, recording
    cameraObject = cv2.VideoCapture(0)
    fps = 30
    frame_count = 0
    recording = True
    raiz.bind("<Key>", record_keyboard)
    capturarImagen()
    # vaciar el contenido del cuadro de texto
    text_input.delete(0,'\n')
    save_text()
   
    
    

def capturarImagen():
    global cameraObject, frame_count, fps, recording
    # verificar objeto
    if cameraObject is not None and recording:
        # captura una imagen
        retval, imagen = cameraObject.read()
        if retval == True:
            frame_count += 1
            # corrección de la inversión de la cámara
            imagen = cv2.flip(imagen, 1)
            # convertir array a imagen Pil
            img = Image.fromarray(imagen)
            img = img.resize((640,480))
            imgTk = ImageTk.PhotoImage(image = img)
            captureLabel.configure(image = imgTk)
            captureLabel.image = imgTk
            captureLabel.after(1000//fps, capturarImagen)
            if frame_count % fps == 0:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                image_path = os.path.join("capturas", f"captura_{current_time}.jpg")
                cv2.imwrite(image_path,imagen)
        else:
            captureLabel.image = ""
            cameraObject.release()

def cerrarFunciones():
    global cameraObject, recording
    captureLabel.image = ""
    cameraObject.release()
    text_input.delete(0, 'end')
    raiz.unbind("<Key>")
    recording = False
    enumerarImagenes()


def cerrarVentana():
    raiz.destroy()

def enumerarImagenes():
    files = os.listdir("capturas")
    files.sort(key=lambda x: os.path.getmtime("capturas/" + x), reverse=True)
    for i, file_name in enumerate(files, start=1):
        print(f"{i}. {file_name}")

# Crear Carpeta para las capturas
if not os.path.exists("capturas"):
    os.mkdir("capturas")

# Crear objeto Ventana
raiz = Tk()
raiz.geometry("640x580")
raiz.title("Capturar imagen")



# frames
captureFrame = Frame()
captureFrame.config(width = "640", heigh = "480")
captureFrame.place(x = 0, y = 0)

textFrame = Frame()
textFrame.config(width = "640", heigh = "50")
textFrame.place(x = 0, y = 480)


btnFrame = Frame()
btnFrame.config(width = "640", heigh = "150")
btnFrame.place(x = 0, y = 530)

captureLabel = Label(captureFrame)
captureLabel.place(x = 0, y = 0)

label = Label(textFrame, text="Enter some text: ")
label.pack(side=LEFT,padx=5)
textFrame.bind("<Key>", record_keyboard)

text_input = Entry(textFrame)
text_input.pack(side=LEFT,padx=5)
text_input.bind('<Return>', iniciarfunciones)
text_input.focus_set()


btnCapture = Button(btnFrame, text = "START", command = iniciarfunciones)
btnCapture.place(x = 20, y = 40)
btnCerrarVideo = Button(btnFrame, text = "Cerrar Camara", command = cerrarFunciones)
btnCerrarVideo.place(x = 300, y = 40)

btnCerrar = Button(btnFrame, text = "Close", command = cerrarVentana)
btnCerrar.place(x = 510, y = 40)

raiz.mainloop()