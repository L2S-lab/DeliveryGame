import time
from robomaster import robot
import keyboard


status = None

def sub_data_handler(sub_info):
    global status 
    status = sub_info

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_arm = ep_robot.robotic_arm
    ep_gripper = ep_robot.gripper

    x_val = 0.3
    y_val = 0.3
    z_val = 30

    ep_gripper.sub_status(freq=5, callback=sub_data_handler)

    while True: 
        # Move in 4 directions
        if keyboard.is_pressed('z'):
            ep_chassis.drive_speed(x=x_val, y=0, z=0, timeout=.5)

        if keyboard.is_pressed('q'):
            ep_chassis.drive_speed(x=0, y=-y_val, z=0, timeout=.5)

        if keyboard.is_pressed('d'):
            ep_chassis.drive_speed(x=0, y=y_val, z=0, timeout=.5)
            
        if keyboard.is_pressed('s'):
            ep_chassis.drive_speed(x=-x_val, y=0, z=0, timeout=.5)
        
        # Rotate robot
        if keyboard.is_pressed('e'):
            ep_chassis.drive_speed(x=0, y=0, z=z_val, timeout=.5)

        if keyboard.is_pressed('a'):
            ep_chassis.drive_speed(x=0, y=0, z=-z_val, timeout=.5)

        if keyboard.is_pressed('p'):
            ep_gripper.close(power=50)
            time.sleep(0.2)
            ep_gripper.pause()

        if keyboard.is_pressed('o'):
            ep_gripper.open(power=50)
            time.sleep(0.2)
            ep_gripper.pause()

        if keyboard.is_pressed('up arrow'):
            ep_arm.move(x=10, y=0).wait_for_completed()

        if keyboard.is_pressed('down arrow'):
            ep_arm.move(x=-10, y=0).wait_for_completed()

        if keyboard.is_pressed('right arrow'):
            ep_arm.move(x=0, y=10).wait_for_completed()

        if keyboard.is_pressed('left arrow'):
            ep_arm.move(x=0 , y=-10).wait_for_completed()

        # Escape the game
        if keyboard.is_pressed('esc'):
            break

    ep_gripper.unsub_status()
    ep_robot.close()
