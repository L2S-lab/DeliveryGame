from robomaster import robot

def connect(conn_type, sn="3JKCH88**1**UF"):
    ep_robot = robot.Robot()
    if conn_type == "ap": #Connection via wifi
       ep_robot.initialize(conn_type="ap")
    else:
        ep_robot.initialize(conn_type="sta", sn=sn)
    return ep_robot
