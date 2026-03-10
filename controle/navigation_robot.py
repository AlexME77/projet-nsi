import time
from gps.gps import GPS

def eviter_obstacle(robot):
    robot.arret()
    time.sleep(0.5)

    robot.arriere()
    time.sleep(0.7)

    robot.droite()
    time.sleep(0.7)

    robot.avant()
    time.sleep(1)

def navigation(robot, get_angle_cible, get_distance_cible, get_angle_actuel, distance_arrivee=1, distance_obstacle=20):
    gps = GPS()
    gps.calibration()

    while True: 

        if distance < distance_arrivee:
            robot.arret()
            print("Arrivé à destination !")
            break

        if robot.distance_obstacle() < distance_obstacle:
            eviter_obstacle(robot)
            orienter_vers_cible(robot, get_angle_cible, get_angle_actuel, seuil_angle=10)
        
        else:
            robot.avant()
        time.sleep(0.1)