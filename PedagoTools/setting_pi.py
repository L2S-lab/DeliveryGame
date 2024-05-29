import tkinter as tk
from tkinter import ttk
import keyboard
import time
import cv2
from math import cos, sin, pi
from robomaster import robot
import numpy as np
import tkinter.font as tkFont

# Characteristics of the camera
X_PHOTO = 1280 #pixels
Y_PHOTO = 720 #pixels
ANGLE_OF_VIEW = 120 #degrees
FOCAL_LENGTH = 514 #m

# Characteristics of the target
TARGET_SIZE = 17e-2 #m

markers = []
ep_chassis = None
ep_vision = None


ROBOT_MAX_SPEED_X = 0.5 #m/s
ROBOT_MAX_SPEED_Y = 0.5

FREQUENCY = 10

# Paramètres du contrôleur PID

# Variables pour le calcul PID
prev_error_x, integral_x = 0, 0
prev_error_y, integral_y = 0, 0

track_marker = True

global entry1, entry2, entry3, entry4
global Kp_x, Ki_x, Kp_y, Ki_y

global pose

class MarkerInfo:
    def __init__(self, x, y, w, h, info):
        """
        `x, y` coordonnées sur l'écran de la caméra
        `w, h` largeur et hauteur du marqueur
        """
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info
    
    def compute_actual_length_to_target(self):
        return FOCAL_LENGTH * TARGET_SIZE / (self._w * X_PHOTO)
    
    def compute_yaw_angle(self):
        return ANGLE_OF_VIEW * (self._x - 1/2) / 180 * pi
    
    def delta_to_self(self):
        length = MarkerInfo.compute_actual_length_to_target(self)
        angle = MarkerInfo.compute_yaw_angle(self)
        return length * cos(angle), length * sin(angle)

def remain_in_speed_bounds_x(speed):
    if abs(speed) > ROBOT_MAX_SPEED_X:
        if speed >= 0:
            return ROBOT_MAX_SPEED_X
        else:
            return - ROBOT_MAX_SPEED_X
    else:
        return speed
    
def remain_in_speed_bounds_y(speed):
    if abs(speed) > ROBOT_MAX_SPEED_Y:
        if speed >= 0:
            return ROBOT_MAX_SPEED_Y
        else:
            return - ROBOT_MAX_SPEED_Y
    else:
        return speed

def on_detect_marker(marker_info):
    number = len(marker_info)
    if number == 0:
        return
    for i in range(number):
        x, y, w, h, info = marker_info[i]
        new_marker_info = MarkerInfo(x, y, w, h, info)
        markers.append(new_marker_info)

def sub_position_handler(position_info):
    global pose
    x, y, z = position_info
    pose = [[],[]]
    pose[0].append(x)
    pose[1].append(y)
    print("chassis position: x:{0}, y:{1}, z:{2}".format(x, y, z))

def go_to_marker(ep_robot):
    global prev_error_x, integral_x, derivative_x
    global prev_error_y, integral_y, derivative_y
    global track_marker
    global count
    global Kp_x, Ki_x, Kp_y, Ki_y
    global pose

    markers.clear()
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_chassis.sub_position(freq=10, callback=sub_position_handler)

    # try:
    ep_camera.start_video_stream(display=False)
    # except Exception as e:
    #     print("pb in read_cv2_image ", e)
    #     ep_camera.start_video_stream(display=False)

    while len(markers)==0:
        ep_vision.sub_detect_info(name="marker", callback=on_detect_marker)
        print("Je n'ai pas détecté de marqueur, j'avance")
        ep_robot.chassis.move(x=0.1, y=0, xy_speed=0.5).wait_for_completed()
    
    print(markers)
    print("sortie du while, début du mvt")
    
    while True :
        info, x, y, w, h = markers[-1]._info, markers[-1]._x, markers[-1]._y, markers[-1]._w, markers[-1]._h
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
        cv2.rectangle(img, markers[-1].pt1, markers[-1].pt2, (255, 255, 255))
        cv2.putText(img, markers[-1].text, markers[-1].center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        # cv2.imshow("Markers", img)
        cv2.waitKey(1)

        delta_x, delta_y = markers[-1].delta_to_self()
        print(f"X  : {delta_x} et Y : {delta_y}")
        print(f"X_center  : {x} et Y_center : {y}")
        error_x = delta_x - 0.45
        error_y = delta_y
        # delta_y -= 0.05

        count = 0

        # Calculer les termes PID pour var_x
        proportional_x = error_x
        integral_x = integral_x + error_x / FREQUENCY
        output_x = Kp_x * proportional_x + Ki_x * integral_x 

        # Calculer les termes PID pour var_y
        proportional_y = error_y
        integral_y = integral_y + error_y / FREQUENCY

        output_y = Kp_y * proportional_y + Ki_y * integral_y
        print("speed x " + str(output_x) + "speed y " + str(output_y))


        x_speed = remain_in_speed_bounds_x(output_x)
        y_speed = remain_in_speed_bounds_y(output_y)
        # print(f"Vitesse x: {x_speed} et Vitesse y : {y_speed}")
        # Appliquer la commande de contrôle
        ep_chassis.drive_speed(x=x_speed, y=y_speed, z=0, timeout=1/FREQUENCY)
        
        # Mise à jour de l'erreur précédente
        prev_error_x = error_x
        prev_error_y = error_y

        if abs(error_x)<0.1 and abs(error_y)<0.07 :
            ep_chassis.unsub_position()
            break
    
    time.sleep(3)
    ep_chassis.move(x=pose[0][-1], y=pose[1][-1], z=0, xy_speed=0.7).wait_for_completed()
    result = ep_vision.unsub_detect_info(name="marker")
    # cv2.destroyAllWindows()
    time.sleep(0.1)
    return None

def action_start():
    global entry1, entry2, entry3, entry4
    global Kp_x, Ki_x, Kp_y, Ki_y

    # Récupérer les valeurs des sliders
    Kp_x = float(entry1.get())
    Kp_y = float(entry2.get())
    Ki_x = float(entry3.get())
    Ki_y = float(entry4.get())

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    go_to_marker(ep_robot)

   
def setup(): 
    global entry1, entry2, entry3, entry4
    
    root = tk.Tk()
    root.title("Jeu de Livraison")

    width=600
    height=500
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    GLabel_362=tk.Label(root)
    GLabel_362["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times',size=28)
    GLabel_362["font"] = ft
    GLabel_362["fg"] = "#333333"
    GLabel_362["justify"] = "center"
    GLabel_362["text"] = "Réglage des coefficients du correcteur PI"
    GLabel_362.place(x=10,y=75,width=596,height=77)

    entry1=tk.Entry(root)
    entry1["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times',size=18)
    entry1["font"] = ft
    entry1["fg"] = "#333333"
    entry1["justify"] = "center"
    entry1["text"] = "KP_x"
    entry1["relief"] = "groove"
    entry1.place(x=160,y=160,width=109,height=38)

    entry3=tk.Entry(root)
    entry3["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times',size=18)
    entry3["font"] = ft
    entry3["fg"] = "#333333"
    entry3["justify"] = "center"
    entry3["text"] = "KI_x"
    entry3["relief"] = "groove"
    entry3.place(x=430,y=160,width=109,height=38)

    entry2=tk.Entry(root)
    entry2["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times',size=18)
    entry2["font"] = ft
    entry2["fg"] = "#333333"
    entry2["justify"] = "center"
    entry2["text"] = "KP_y"
    entry2["relief"] = "groove"
    entry2.place(x=160,y=230,width=109,height=38)

    entry4=tk.Entry(root)
    entry4["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times',size=18)
    entry4["font"] = ft
    entry4["fg"] = "#333333"
    entry4["justify"] = "center"
    entry4["text"] = "KI_y"
    entry4.place(x=430,y=230,width=109,height=38)

    GLabel_459=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    GLabel_459["font"] = ft
    GLabel_459["fg"] = "#333333"
    GLabel_459["justify"] = "center"
    GLabel_459["text"] = "KP_x"
    GLabel_459.place(x=70,y=170,width=70,height=25)

    GLabel_126=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    GLabel_126["font"] = ft
    GLabel_126["fg"] = "#333333"
    GLabel_126["justify"] = "center"
    GLabel_126["text"] = "KI_x"
    GLabel_126.place(x=330,y=170,width=70,height=25)

    GLabel_480=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    GLabel_480["font"] = ft
    GLabel_480["fg"] = "#333333"
    GLabel_480["justify"] = "center"
    GLabel_480["text"] = "KP_y"
    GLabel_480.place(x=70,y=240,width=70,height=25)

    GLabel_298=tk.Label(root)
    ft = tkFont.Font(family='Times',size=18)
    GLabel_298["font"] = ft
    GLabel_298["fg"] = "#333333"
    GLabel_298["justify"] = "center"
    GLabel_298["text"] = "KI_y"
    GLabel_298.place(x=330,y=240,width=70,height=25)

    GButton_240=tk.Button(root)
    GButton_240["bg"] = "#efefef"
    ft = tkFont.Font(family='Times',size=18)
    GButton_240["font"] = ft
    GButton_240["fg"] = "#000000"
    GButton_240["justify"] = "center"
    GButton_240["text"] = "Start"
    GButton_240.place(x=250,y=300,width=122,height=48)
    GButton_240["command"] = action_start
    
    GMessage_97=tk.Label(root, wraplength=500)
    ft = tkFont.Font(family='Times',size=10)
    GMessage_97["font"] = ft
    GMessage_97["fg"] = "#333333"
    GMessage_97["justify"] = "left"
    GMessage_97["text"] = "Rappel : Si on augmente la valeur de Kp, on gagne en rapidité mais on perd en précision. Si on augmente la valeur de Ki, on perd en précision et en stabilité. "
    GMessage_97.place(x=40,y=350,height=160)

    image = tk.PhotoImage(file="/Users/alexishanne/Desktop/Projet S8/jeu-robots/Pedago/CS.png")
    image_resized = image.subsample(6, 6)  # Les arguments sont les facteurs de réduction pour la largeur et la hauteur
    image_label = tk.Label(root, image=image_resized)
    image_label.place(x=0, y=0)

    image2 = tk.PhotoImage(file="/Users/alexishanne/Desktop/Projet S8/jeu-robots/Pedago/L2S.png")
    image_resized2 = image2.subsample(9, 9)  # Les arguments sont les facteurs de réduction pour la largeur et la hauteur
    image_label2 = tk.Label(root, image=image_resized2)
    image_label2.place(x=400, y=0)

    root.mainloop()

if __name__=='__main__':
    setup()