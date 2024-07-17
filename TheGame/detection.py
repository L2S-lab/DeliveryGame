import cv2
from math import cos, sin, pi
import numpy as np
import imutils


# Caractéristiques de la balle de tennis
# Définir les plages de couleur pour la balle de tennis en HSV
lower_yellow_green = np.array([16,72,170])
#lower_yellow_green = np.array([29,86,6])
upper_yellow_green = np.array([38,255,250])
#upper_yellow_green = np.array([64,255,255  ])
BALL_SIZE = 6.5e-2 #m

# Caractéritiques du robot
ROBOT_MAX_SPEED_X = 2.5 #m/s
ROBOT_MAX_SPEED_Y = 0.25 #m/s

# Caractéristiques de la caméra
CAMERA_SCREEN_WIDTH = 1280 #pixels
CAMERA_SCREEN_HEIGHT = 720 #pixels
CAMERA_ANGLE_OF_VIEW = 120 #degrés
CAMERA_FOCAL_LENGTH = 514 #mesuré au préalable

x_center, y_center, width, height = 10, 10, 10, 10

def compute_actual_length_to_target(radius):
    """`radius` largeur de l'objet (en pixels)"""
    return CAMERA_FOCAL_LENGTH * BALL_SIZE / (2 * radius)

def compute_yaw_angle(x_center):
    """`x_center` position horizontale du centre de l'objet (en pixels)"""
    theta_degres = CAMERA_ANGLE_OF_VIEW * (x_center / CAMERA_SCREEN_WIDTH - 1/2) 
    theta_rads = theta_degres / 180 * pi
    return  theta_degres, theta_rads

def delta_to_self(x, y, radius):
    length = compute_actual_length_to_target(radius)
    angle = compute_yaw_angle(x)[1]
    return length * cos(angle), length * sin(angle)

def remain_in_speed_bounds_x(speed):
    """Pour s'assurer que le robot se déplace à une vitesse inférieure à ses limites techniques"""
    if abs(speed) > ROBOT_MAX_SPEED_X:
        if speed >= 0:
            return ROBOT_MAX_SPEED_X
        else:
            return -ROBOT_MAX_SPEED_X
    else:
        return speed
    
def remain_in_speed_bounds_y(speed):
    """Pour s'assurer que le robot se déplace à une vitesse inférieure à ses limites techniques"""
    if abs(speed) > ROBOT_MAX_SPEED_Y:
        if speed >= 0:
            return ROBOT_MAX_SPEED_Y
        else:
            return -ROBOT_MAX_SPEED_Y
    else:
        return speed

def detect_ball(frame):
    success = False
    x, y, radius = 0, 0, 0
    # Flouter l'image pour éviter les bruits
    frame = cv2.GaussianBlur(frame, (11,11), 0)
    # Convertir l'image en couleur RGB en HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Filtrer l'image pour obtenir uniquement les pixels vert jaune
    mask = cv2.inRange(hsv, lower_yellow_green, upper_yellow_green)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    # Trouver les contours dans l'image
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) == 0:
        success = False
    else:
        largest_contour = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        M = cv2.moments(largest_contour)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        if radius < 10: #L'objet détecté est trop petit, il s'agit probablement d'un bruit de mesure
            success = False
        else:
            success = True
            #cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            #cv2.circle(frame, center, 5, (0,0,255), 2)

    return  success, x, y, radius
