import time
import keyboard
import cv2
from math import cos, sin, pi
import numpy as np
import imutils


# Caractéristiques de la balle de tennis
# Définir les plages de couleur pour la balle de tennis en HSV
lower_yellow_green = np.array([16,72,170])
upper_yellow_green = np.array([38,255,250])
BALL_SIZE = 6.5e-2 #m

# Caractéritiques du robot
ROBOT_MAX_SPEED_X = 2.5 #m/s
ROBOT_MAX_SPEED_Y = 0.25 #m/s

# Caractéristiques de la caméra
CAMERA_SCREEN_WIDTH = 1280 #pixels
CAMERA_SCREEN_HEIGHT = 720 #pixels
CAMERA_ANGLE_OF_VIEW = 120 #degrés
CAMERA_FOCAL_LENGTH = 514 #mesuré au préalable

# Paramètres du contrôleur PI
Kp_x, Ki_x = 1.0 , 0.038
Kp_y, Ki_y = 5.0, 0.038

# Variables pour le calcul du PI
prev_error_x, integral_x = 0, 0
prev_error_y, integral_y = 0, 0

#Fréquence de mise à jour
FREQUENCY = 10

#count 
count = 0

x_center, y_center, width, height = 10, 10, 10, 10

track_ball = True

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
            return - ROBOT_MAX_SPEED_X
    else:
        return speed
    
def remain_in_speed_bounds_y(speed):
    """Pour s'assurer que le robot se déplace à une vitesse inférieure à ses limites techniques"""
    if abs(speed) > ROBOT_MAX_SPEED_Y:
        if speed >= 0:
            return ROBOT_MAX_SPEED_Y
        else:
            return - ROBOT_MAX_SPEED_Y
    else:
        return speed

def on_detect_ball(ep_chassis, x, y, radius):
    """Calcul du contrôleur PI à partir des données de la balle détectée"""
    global prev_error_x, integral_x
    global prev_error_y, integral_y
    global track_ball
    global count
    var_x, var_y = delta_to_self(x, y, radius)
    error_x = var_x - 0.2 #Pour prendre en compte la taille du panier
    error_y = var_y - 0 #Pour prendre en compte la taille du panier

    #Détecter si la balle est dans la pince
    #Les valeurs on été choisies empiriquement
    x_min = int(CAMERA_SCREEN_WIDTH * 0.38)  # Exclure 38% de la largeur de l'image du côté gauche
    x_max = int(CAMERA_SCREEN_WIDTH * 0.62)  # Exclure 38% de la largeur de l'image du côté droit 
    y_min = int(CAMERA_SCREEN_HEIGHT * 0.7) # Commencer à 70% de la hauteur de l'image
    y_max = int(CAMERA_SCREEN_HEIGHT)
    if x_min <= int(x) <= x_max and y_min <= int(y) <= y_max:
        ep_chassis.drive_speed(x=0, y=0, z=0, timeout=1/FREQUENCY)
        count += 1
        if count == 10:
            track_ball = False
    else:
        count = 0

        # Calculer les termes PI pour var_x
        proportional_x = error_x
        integral_x = integral_x + error_x / FREQUENCY
        derivative_x = (error_x - prev_error_x) * FREQUENCY
        output_x = Kp_x * proportional_x + Ki_x * integral_x 

        # Calculer les termes PI pour var_y
        proportional_y = error_y
        integral_y = integral_y + error_y / FREQUENCY
        derivative_y = (error_y - prev_error_y) * FREQUENCY
        output_y = Kp_y * proportional_y + Ki_y * integral_y

        x_speed = remain_in_speed_bounds_x(output_x)
        y_speed = remain_in_speed_bounds_y(output_y)
        # Appliquer la commande de contrôle
        ep_chassis.drive_speed(x=x_speed, y=y_speed, z=0, timeout=1/FREQUENCY)
        
        # Mise à jour de l'erreur précédente
        prev_error_x = error_x
        prev_error_y = error_y

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
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), 2)

    return  success, x, y, radius, frame

def has_catched(ep_robot):
    ep_camera = ep_robot.camera
    try:
        img = ep_camera.read_cv2_image(strategy="newest", timeout=3)
    except Exception as e:
        print("erreur dans le chargement d'image ", e)
        return False

    ball_on_screen, x, y, _, _ = detect_ball(img)

    height, width, _ = img.shape

    # Coordonnées du rectangle de détection de la pince
    x_min = int(width * 0.38)  # Exclure 38% de la largeur de l'image du côté gauche
    x_max = int(width * 0.62)  # Exclure 38% de la largeur de l'image du côté droit
    y_min = int(height * 0.7)  # Commencer à 75% de la hauteur de l'image
    y_max = int(height)  
    
    if ball_on_screen and x_min <= int(x) <= x_max and y_min <= int(y) <= y_max:
        print("Good")
        return True
    x1 = int(width * 0.38)  # Exclure 10% de la largeur de l'image du côté gauche
    x2 = int(width * 0.62)  # Exclure 10% de la largeur de l'image du côté droit
    y1 = int(height)  # Commencer à 80% de la hauteur de l'image
    y2 = int(height * 0.75)
    cv2.destroyAllWindows()
    cv2.waitKey(10)
    # ep_robot.camera.stop_video_stream()
    if ball_on_screen:
        if x1 <= int(x) <= x2 and y2 <= int(y) <= y1:
            print("Good")
            cv2.destroyAllWindows()
            cv2.waitKey(10)
            return True
    cv2.destroyAllWindows()
    cv2.waitKey(10)
    return False

def go_to_ball(ep_robot):
    global track_ball
    global prev_error_x, integral_x
    global prev_error_y, integral_y
    track_ball = True
    prev_error_x, integral_x = 0, 0
    prev_error_y, integral_y = 0, 0

    ep_chassis = ep_robot.chassis
    ep_camera = ep_robot.camera

    while True: 
        try:
            img = ep_camera.read_cv2_image(strategy="newest", timeout=3)
        except Exception as e:
            print("erreur connexion camera ", e)
            continue
        cv2.waitKey(10)
        height, width, _ = img.shape

        # Coordonnées du coin supérieur gauche et du coin inférieur droit du rectangle
        x1 = int(width * 0.38)  # Exclure 10% de la largeur de l'image du côté gauche
        x2 = int(width * 0.62)  # Exclure 10% de la largeur de l'image du côté droit
        y1 = int(height)  # Commencer à 80% de la hauteur de l'image
        y2 = int(height * 0.75)  # Monter jusqu'à 60% de la hauteur de l'image

        # Dessiner le rectangle sur l'image
        color = (0, 255, 0)  # Couleur du rectangle en BGR (ici, vert)
        thickness = 2  # Épaisseur du trait
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        
        if track_ball:
            ball_on_screen, x, y, radius, _ = detect_ball(img)

            if ball_on_screen:
                on_detect_ball(ep_chassis, x, y, radius)
                # Afficher un cercle autour de la balle
                cv2.circle(img, (int(x), int(y)), int(radius), (0,255,255), 2)
                cv2.circle(img, (int(x), int(y)), 5, (255,0,0), thickness)
        else:
            break
    
        cv2.imshow("Detect a Tennis Ball", img)    
        cv2.waitKey(10)

        # Pour arrêter de traquer la balle
        if keyboard.is_pressed('space'):
            track_ball = not track_ball

        # Arrêter le jeu
        if keyboard.is_pressed('esc'):
            break
    
    cv2.destroyAllWindows()
