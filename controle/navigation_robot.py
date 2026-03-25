import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
from gps.gps import GPS
from gps.database import coord_destination
from robot import Robot

def eviter_obstacle(robot, direction="droite"):
    print("Début de l'évitement d'obstacle")

    robot.arret()
    time.sleep(0.5)

    robot.arriere()
    time.sleep(0.7)

    if direction == "droite":
        robot.droite()
    else:
        robot.gauche()
    time.sleep(0.7)

    robot.avant()
    time.sleep(1)

    print("Fin de l'évitement d'obstacle")

def navigation(robot, points):
    
    gps = GPS()

    seuil_arrivee = 2.0
    seuil_obstacle = 20
    i=0
    fin = False
    orientation_robot = gps.angle_depart(robot)

    while not fin:
        
        position = gps.get_position_robot()
        if position is None:
            print("Erreur GPS")
            robot.arret()
            break

        "Récupération de la distance à la cible"
        distance_arrivee = gps.distance_2pGPS(position, points[i])

        print("Vérification de la distance à la cible")
        if distance_arrivee < seuil_arrivee:
            robot.arret()
            print("Point atteint")
            print("Vérification de l'arrivée à la cible")
            if i < len(points)-1:
                print("Passage au point suivant")
                i += 1
                continue
            else:
                print("Parcours terminé")
                fin = True
                return

        print("Calcul de l'orientation")
        orientation_voulue = gps.get_orientation(position, points[i])
        correction = orientation_voulue - orientation_robot
        facteur_rotation = 0.01  # Ajuster ce facteur pour trouver le bon temps de rotation en fonction de l'orientation
        if correction > 180:
            correction -= 360
        if correction < -180:
            correction += 360

        print("Correction de l'orientation")
        if -5 < correction < 5:
            robot.avant()
            time.sleep(1)
            continue
        elif correction < 0:
                robot.rotation_trigo()
        else:
            robot.rotation_horaire()
        time.sleep(abs(correction) * facteur_rotation)

        orientation_robot = gps.get_orientation(position, points[i])

        print("Vérification de la présence d'obstacles")
        distance_obstacle = robot.distance_obstacle()
        if distance_obstacle is not None and distance_obstacle < seuil_obstacle:
            print("Évitement de l'obstacle")
            eviter_obstacle(robot, direction="droite" if correction > 0 else "gauche")
            continue
        else:
            print("Avance vers la cible ")
            robot.avant()
        time.sleep(1)

if __name__ == '__main__':
    robot = Robot()
    navigation(robot, [(12.0, 24.0)])

