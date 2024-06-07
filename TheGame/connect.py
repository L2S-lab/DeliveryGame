from robomaster import robot

def connect(conn_type, sn):
    ep_robot = robot.Robot()
    if conn_type == "ap": #Connection via wifi
       ep_robot.initialize(conn_type="ap")
    else:
        ep_robot.initialize(conn_type="sta", sn="3JKCH8800100UF")

    return ep_robot
