import pyjoystick
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
from robomaster import robot
from numpy import sqrt, sign
import keyboard
import time
import cv2

echap = False

def joystick_curve(value):
    return sign(value) * sqrt(abs(value))

def handle_key_event(key):
    global echap
    # print(key, '-', key.keytype, '-', key.number, '-', key.value)

    if key in ["Axis 1", "-Axis 1"]:
        ep_chassis.drive_speed(x=-joystick_curve(key.value), y=0, z=0, timeout=.2)
    if key in ["Axis 0", "-Axis 0"]:
        ep_chassis.drive_speed(x=0, y=joystick_curve(key.value), z=0, timeout=.2)

    if key == "Hat 0 [Up]":
        ep_chassis.drive_speed(x=x_val, y=0, z=0, timeout=.2)

    if key == "Hat 0 [Left]":
        ep_chassis.drive_speed(x=0, y=-y_val, z=0, timeout=.2)

    if key == "Hat 0 [Right]":
        ep_chassis.drive_speed(x=0, y=y_val, z=0, timeout=.2)
            
    if key == "Hat 0 [Down]":
        ep_chassis.drive_speed(x=-x_val, y=0, z=0, timeout=.2)

    if key == "Button 1":
        ep_gripper.close(power=50)
        time.sleep(0.1)
        ep_gripper.pause()

    if key == "Button 0":
        ep_gripper.open(power=50)
        time.sleep(0.1)
        ep_gripper.pause()

    if key == "Button 2":
        ep_arm.moveto(x=105, y=100).wait_for_completed()
        
    if key == "Button 3":
        ep_arm.moveto(x=205, y=-50).wait_for_completed()
        time.sleep(0.2)

    if key == "Button 4":
        ep_chassis.drive_speed(x=0, y=0, z=-z_val, timeout=.2)

    if key == "Button 5":
        ep_chassis.drive_speed(x=0, y=0, z=z_val, timeout=.2)

    if key == "Button 10":
        echap = True

# If it button is held down it should be repeated
repeater = pyjoystick.Repeater(first_repeat_timeout=0.1, repeat_timeout=0.2, check_timeout=0.2)


mngr = pyjoystick.ThreadEventManager(event_loop=run_event_loop,
                                     handle_key_event=handle_key_event,
                                     button_repeater=repeater)

if __name__ == "__main__":
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper

    x_val = 0.1
    y_val = 0.1
    z_val = 30

    img = cv2.imread("Interface-Controle-Robot.jpg")
    cv2.namedWindow("Controles", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Controles",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    mngr.start()
    while True:
        cv2.imshow("Controles", img)
        cv2.waitKey(1)
        if echap or keyboard.is_pressed('esc'):
            break
    cv2.destroyAllWindows()
    ep_gripper.unsub_status()
    ep_robot.close()
