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

#parcours c'est quoi ? une liste de points GPS ? Déjà en lattitude longitude ?
def navigation(robot, points):
    
    gps = GPS()

    seuil_arrivee = 2.0
    seuil_obstacle = 20
    i=0
    fin = False

    while not fin: 

        "Récupération de la distance à la cible"
        distance_arrivee = gps.get_distance_cible(points, ordre=i)

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
        orientation = gps.correction_orientation(points, i)

        print("Correction de l'orientation")
        if orientation > -5 and orientation < 5:
            continue
        elif orientation < 0:
                robot.rotation_trigo()
        else:
            robot.rotation_horaire()    
        time.sleep(abs(orientation/30))  # Ajuster le temps de rotation en fonction de l'orientation (trouver la bonne valeur et faire attention à la vitesse garder toujours la même)
# On peut même faire une fonction ou une relation qui calcule le temps de rotation en fonction de l'orientation et de la vitesse du robot

        print("Vérification de la présence d'obstacles")
        if robot.distance_obstacle() < seuil_obstacle:
            
            print("Obstacle détecté, calcul de la  direction d'évitement")
            orientation = gps.correction_orientation(points, i)

            print("Évitement de l'obstacle")
            eviter_obstacle(robot, direction="droite" if orientation > 0 else "gauche")

        else:
            print("Avance vers la cible ")
            robot.avant()
        time.sleep(1)

if __name__ == '__main__':
    robot = Robot()
    navigation(robot, [(12.0, 24.0)])

