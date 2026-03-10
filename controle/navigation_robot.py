import time
from gps.gps import GPS
from gps.database import lire_destination

def eviter_obstacle(robot):
    robot.arret()
    time.sleep(0.5)

    robot.arriere()
    time.sleep(0.7)

    robot.droite()
    time.sleep(0.7)

    robot.avant()
    time.sleep(1)

def navigation(robot, seuil_obstacle=20, seuil_arrivee=0.5):
    gps = GPS()
    gps.port()
    gps.calibration()

    
    while True: 

        distance_arrivee = gps.distance_2pGPS(gps.lire_position_GPS(), lire_destination("test", ordre=1))
        if distance_arrivee < seuil_arrivee:
            robot.arret()
            print("Point atteint")
            break

        if robot.distance_obstacle() < seuil_obstacle:
            eviter_obstacle(robot)
            gps.orientation(gps.lire_position_GPS(), lire_destination("test", ordre=1))
        
        else:
            robot.avant()
        time.sleep(0.1)