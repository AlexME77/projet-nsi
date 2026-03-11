import time
from gps.gps import GPS
from gps.database import coord_destination

def eviter_obstacle(robot, direction="droite"):
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

#parcours c'est quoi ? une liste de points GPS ? Déjà en lattitude longitude ?
def navigation(robot, parcours):
    
    gps = GPS()
    orientation_depart = gps.angle_depart()

    seuil_arrivee = 2.0
    seuil_obstacle = 20
    i=0
    fin = False

    while not fin: 

        distance_arrivee = gps.get_distance_cible(parcours, ordre=i)
        if distance_arrivee < seuil_arrivee:
            robot.arret()
            print("Point atteint")
            if i < len(parcours)-1:
                i += 1
                break
            else:
                print("Parcours terminé")
                fin = True
                break

        if robot.distance_obstacle() < seuil_obstacle:
            
            orientation = gps.get_orientation(gps.get_position_robot(), coord_destination(parcours, ordre=i))

            eviter_obstacle(robot, direction="droite" if orientation < 180 else "gauche")

            orientation = gps.get_orientation(gps.get_position_robot(), coord_destination(parcours, ordre=i))

            if orientation < 180:
                robot.rotation_trigo()

            else:
                robot.rotation_horaire()
            
            time.sleep(orientation/30)  # Ajuster le temps de rotation en fonction de l'orientation (trouver la bonne valeur et faire attention à la vitesse garder toujours la même)
# On peut même faire une fonction ou une relation qui calcule le temps de rotation en fonction de l'orientation et de la vitesse du robot

        else:
            robot.avant()
        time.sleep(0.1)