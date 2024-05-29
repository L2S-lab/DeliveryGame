import keyboard
import time
import cv2
from math import cos, sin, pi

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
Kp_x, Ki_x, Kd_x = 1.0 , 0, 0.01
Kp_y, Ki_y, Kd_y = 0.5, 0.01, 0.01

# Variables pour le calcul PID
prev_error_x, integral_x, derivative_x = 0, 0, 0
prev_error_y, integral_y, derivative_y = 0, 0, 0

track_marker = True

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

def go_to_marker(ep_robot):
    global prev_error_x, integral_x, derivative_x
    global prev_error_y, integral_y, derivative_y
    global track_marker
    global count
    markers.clear()
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis

    # try:
    #     ep_camera.start_video_stream(display=False)
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
        img = ep_camera.read_cv2_image(strategy="newest", timeout=3)
        cv2.rectangle(img, markers[-1].pt1, markers[-1].pt2, (255, 255, 255))
        cv2.putText(img, markers[-1].text, markers[-1].center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.imshow("Markers", img)
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
        derivative_x = (error_x - prev_error_x) * FREQUENCY
        # output_x = Kp_x * proportional_x + Ki_x * integral_x + Kd_x * derivative_x
        output_x = Kp_x * proportional_x + Ki_x * integral_x 

        # Calculer les termes PID pour var_y
        proportional_y = error_y
        integral_y = integral_y + error_y / FREQUENCY
        derivative_y = (error_y - prev_error_y) * FREQUENCY

        # output_y = Kp_y * proportional_y + Ki_y * integral_y + Kd_y * derivative_y
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
            break
        
    print("marker:{0} x:{1}, y:{2}, w:{3}, h:{4}".format(info, x, y, w, h))
    print("fini mvt")
    time.sleep(0.1)
    result = ep_vision.unsub_detect_info(name="marker")
    print("fini unsub")
    time.sleep(0.1)
    cv2.destroyAllWindows()
    # ep_camera.stop_video_stream()
    time.sleep(0.1)
    print("fin video stream")
    return None