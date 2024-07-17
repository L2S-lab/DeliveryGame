import time


def initiate_pos(ep_arm):
    """Position par défaut de la pince en l'air"""
    ep_arm.moveto(x=105, y=100).wait_for_completed()
    time.sleep(0.2)

def set_default_state_gripper(ep_gripper, ep_arm):
    """Position par défaut de la pince au sol""" 
    initiate_pos(ep_arm)
    ep_gripper.open(power=50)
    time.sleep(1)
    ep_gripper.pause()

    ep_arm.moveto(x=205, y=-50).wait_for_completed()
    time.sleep(0.2)

def catch(ep_gripper):
    """Fermer la pince pour attrapper un objet"""
    ep_gripper.close(power=50)
    time.sleep(1)
    ep_gripper.pause()

def drop_ball(ep_gripper,ep_arm):
    """Lâcher l'objet tenu en ouvrant la pince"""
    initiate_pos(ep_arm)
    ep_arm.move(x=100, y=0).wait_for_completed()
    time.sleep(0.2)
    ep_gripper.open(power=50)

    time.sleep(1)
    ep_gripper.pause()
