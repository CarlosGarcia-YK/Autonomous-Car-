import serial
import tkinter as tk
import keyboard
import time
import cv2  # opencv
import urllib.request  # Open and Read URL
import numpy as np
from PIL import ImageTk
from PIL import Image
import threading

# Configure serial connection with Arduino
ser = serial.Serial()


# Function to obtain the entry text value and configure the serial connection
def connect_serial():
    port = port_entry.get()
    ser.port = port
    ser.baudrate = 9600
    ser.timeout = 1
    ser.open()

    # Data reading from Arduino starts in background
    #read_thread = threading.Thread(target=read_serial, daemon=True)
    #read_thread.start()

    # The detection of pressed keys starts in background
    send_thread = threading.Thread(target=send_message, daemon=True)
    send_thread.start()

    # Focusing on "Connect" button is established
    toggle_button.focus_set()


# Video file is opened
video = cv2.VideoWriter('test2.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (320, 240))

# Global variables for video
is_running = True
is_video_on = True
video_thread = None

# Global variables for keys
last_pressed_key = "None"
last_release_time = time.time()
last_sent_message = ""


# Video file is opened
def start_recording():
    video = cv2.VideoWriter('test2.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (320, 240))
    while is_running:
        if is_video_on:
            # Image is captured from URL
            url = get_url()
            img_resp = urllib.request.urlopen(url)
            img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)

            # Frame is added
            video.write(img)

    # Releases the video
    video.release()


# Function to alternate the state of the video
def toggle_video():
    global is_video_on, video_thread
    is_video_on = not is_video_on

    if not is_video_on and video_thread is not None:
        # Video playing is stopped
        global is_running
        is_running = False
        video_thread.join()
        video_thread = None

    if is_video_on and video_thread is None:
        # Video recording starts in background
        is_running = True
        video_thread = threading.Thread(target=start_recording)
        video_thread.start()


# Function to obtain URL from text entry
def get_url():
    return url_entry.get()


# Window of the interface is created
root = tk.Tk()
root.geometry("800x600")
root.title("Control for Motor and Servo")


# Entry text to read COM value
port_entry = tk.Entry(root)
port_entry.pack(side=tk.TOP)


# Label for the URL
url_label = tk.Label(root, text="Camera URL:")
url_label.pack(side=tk.TOP)

# Entry label to add the URL
url_entry = tk.Entry(root)
url_entry.pack(side=tk.TOP)

# Button to establish serial communication
connect_button = tk.Button(root, text="Connect", command=connect_serial)
connect_button.pack()

# Variables for motor, angle, and speed
value = tk.StringVar()
angle = tk.StringVar()
velocity = tk.StringVar()


# Function to read values from Arduino and update of variables
def read_serial():
    data = ser.readline().decode(errors='ignore').strip().split(",")
    if len(data) == 3:
        value.set(data[0])
        angle.set(data[1])
        velocity.set(data[2])
    root.after(1, read_serial)


# Function to dispatch string with the speed value
def set_speed(read_value):
    outgoing_data = bytes("speed" + str(read_value) + "\n", 'utf-8')
    ser.write(outgoing_data)


# Function to start the function to send speed data
def set_speed_thread(read_value):
    thread = threading.Thread(target=set_speed, args=(read_value,), daemon=True)
    thread.start()


# Function to send messages to Arduino
def send_message():
    global last_pressed_key, last_release_time, last_sent_message

    # If last pressed key is unpressed, redefine the state
    if last_pressed_key != "None" and not keyboard.is_pressed(last_pressed_key):
        last_release_time = time.time()
        last_pressed_key = "None"
        UP_Button.config(bg="blue")
        DOWN_Button.config(bg="blue")

    # If no key is pressed and delay time has passed since the last key is pressed, it returns to center value
    if last_pressed_key == "None" and time.time() - last_release_time >= 0.01:
        new_message = "CENTER"
        if new_message != last_sent_message:
            # Message is sent through serial
            ser.write((new_message + '\n').encode())

            last_sent_message = new_message

    # If no key is pressed, verify if any key is pressed
    if last_pressed_key == "None":
        if keyboard.is_pressed("w"):
            print("w",time.strftime('%Y%m%d_%H%M%S'))
            last_pressed_key = "w"
            UP_Button.config(bg="red")
            DOWN_Button.config(bg="blue")
        elif keyboard.is_pressed("s"):
            print("s",time.strftime('%Y%m%d_%H%M%S'))
            last_pressed_key = "s"
            UP_Button.config(bg="blue")
            DOWN_Button.config(bg="red")
    # If last key is still pressed
    else:
        new_message = ""
        if last_pressed_key == "w":
            print("w",time.strftime('%Y%m%d_%H%M%S'))
            new_message = "UP"
            UP_Button.config(bg="red")
            DOWN_Button.config(bg="blue")
        elif last_pressed_key == "s":
            print("s",time.strftime('%Y%m%d_%H%M%S'))
            new_message = "DOWN"
            UP_Button.config(bg="blue")
            DOWN_Button.config(bg="red")
        if new_message != last_sent_message:
            ser.write((new_message + '\n').encode())
            last_sent_message = new_message
    # Messages are sent if direction keys are pressed
    if keyboard.is_pressed("a"):
        if not keyboard.is_pressed("d"):
            time.sleep(0.1)
            ser.write("LEFT\n".encode())
            LEFT_Button.config(bg="red")
            RIGHT_Button.config(bg="blue")
            print("a",time.strftime('%Y%m%d_%H%M%S'))
    elif keyboard.is_pressed("d"):
        if not keyboard.is_pressed("a"):
            time.sleep(0.1)
            ser.write("RIGHT\n".encode())
            RIGHT_Button.config(bg="red")
            LEFT_Button.config(bg="blue")
            print("d",time.strftime('%Y%m%d_%H%M%S'))
    # Function is executed each 50 ms
    root.after(50, send_message)


# Function to update frame of video
def update_video():
    global is_running, is_video_on

    # If is_video_on is false, show a fixed image
    if not is_video_on:
        url = get_url()
        img_resp = urllib.request.urlopen(url)
        img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)

        # Muestra el frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(img))
        video_label.configure(image=img)
        video_label.image = img  # Image cannot be deleted
    else:
        # Anything is shown
        pass

    # If is_running is True, function is called each ms
    if is_running:
        root.after(1, update_video)


# Images are inserted to show the state of the keys
UP = tk.PhotoImage(file="UP.png")
DOWN = tk.PhotoImage(file="DOWN.png")
RIGHT = tk.PhotoImage(file="RIGHT.png")
LEFT = tk.PhotoImage(file="LEFT.png")
UP_Button = tk.Label(root, image=UP, height=30, width=30, \
    bg="blue")
UP_Button.place(x=326, y=300)
DOWN_Button = tk.Label(root, image=DOWN, height=30, width=30, bg="blue")
DOWN_Button.place(x=326, y=400)
RIGHT_Button = tk.Label(root, image=RIGHT, height=30, width=30, bg="blue")
RIGHT_Button.place(x=376, y=350)
LEFT_Button = tk.Label(root, image=LEFT, height=30, width=30, bg="blue")
LEFT_Button.place(x=276, y=350)


# Labels for motor value, angle, and speed
value_label = tk.Label(root, text="Motor Value:")
value_label.pack()
value_label.place(x=80, y=340)
value_display = tk.Label(root, textvariable=value)
value_display.pack()
value_display.place(x=110, y=360)

angle_label = tk.Label(root, text="Servo Angle:")
angle_label.pack()
angle_label.place(x=80, y=380)
angle_display = tk.Label(root, textvariable=angle)
angle_display.pack()
angle_display.place(x=120, y=400)

velocity_label = tk.Label(root, text="Speed:")
velocity_label.pack()
velocity_label.place(x=80, y=420)
velocity_display = tk.Label(root, textvariable=velocity)
velocity_display.pack()
velocity_display.place(x=115, y=440)

# Button to turn on/off the video
toggle_button = tk.Button(root, text="STOP-PLAY", command=toggle_video)
toggle_button.pack(side=tk.BOTTOM)
toggle_button.place(x=80, y=290)

# Label for the frame of the video
video_label = tk.Label(root)
video_label.place(x=100, y=25)

# Velocity bar is created
speed_value = tk.StringVar()
Speed = tk.Scale(root, label="Speed", from_=0, to=100, orient=tk.VERTICAL, variable=speed_value, sliderlength=30, length=150, command=set_speed_thread)
Speed.place(x=435, y=290)


# Graphic interface is executed
root.mainloop()

# When window is closed, the serial communication ends
ser.close()
