from robomaster import robot
import time


def sub_data_handler(sub_info):
    pos_x, pos_y = sub_info
    print("Robotic Arm: pos x:{0}, pos y:{1}".format(pos_x, pos_y))

def initiate_pos(ep_robot):
    """Position par défaut de la pince en l'air"""
    ep_arm = ep_robot.robotic_arm
    ep_arm.moveto(x=105, y=100).wait_for_completed()
    time.sleep(0.2)

def set_default_state_gripper(ep_robot):
    """Position par défaut de la pince au sol"""
    ep_gripper = ep_robot.gripper
    ep_arm = ep_robot.robotic_arm
    initiate_pos(ep_robot)
    ep_gripper.open(power=50)
    time.sleep(2)
    ep_gripper.pause()

    ep_arm.moveto(x=205, y=-50).wait_for_completed()
    time.sleep(0.2)

def catch(ep_robot):
    """Fermer la pince pour attrapper un objet"""
    ep_gripper = ep_robot.gripper
    ep_gripper.close(power=50)
    time.sleep(2)
    ep_gripper.pause()

def drop_ball(ep_robot):
    """Lâcher l'objet tenu en ouvrant la pince"""
    ep_gripper = ep_robot.gripper
    ep_arm = ep_robot.robotic_arm
    initiate_pos(ep_robot)
    ep_arm.move(x=100, y=0).wait_for_completed()
    time.sleep(0.2)
    ep_gripper.open(power=50)
    time.sleep(2)
    ep_gripper.pause()
