import keyboard
import time
import cv2
from math import cos, sin, pi

# Caractéristiques de la caméra
X_PHOTO = 1280 #pixels
Y_PHOTO = 720 #pixels
ANGLE_OF_VIEW = 120 #degrés
FOCAL_LENGTH = 514 #Mesuré au préalable

# Caractéristiques du marqueur
TARGET_SIZE = 17e-2 #m

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
