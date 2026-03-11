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
def navigation(robot, nom_parcours):
    
    points_parcours = coord_destination(nom_parcours)

    gps = GPS()

    seuil_arrivee = 2.0
    seuil_obstacle = 20
    i=1
    fin = False

    while not fin: 

        distance_arrivee = gps.get_distance_cible(nom_parcours, ordre=i)

        orientation = gps.correction_orientation(nom_parcours, i)
        if orientation < 0:
                robot.rotation_trigo()
        else:
            robot.rotation_horaire()    
        time.sleep(orientation/30)  # Ajuster le temps de rotation en fonction de l'orientation (trouver la bonne valeur et faire attention à la vitesse garder toujours la même)
# On peut même faire une fonction ou une relation qui calcule le temps de rotation en fonction de l'orientation et de la vitesse du robot

        if distance_arrivee < seuil_arrivee:
            robot.arret()
            print("Point atteint")
            if i < len(points_parcours):
                i += 1
                break
            else:
                print("Parcours terminé")
                fin = True
                break

        if robot.distance_obstacle() < seuil_obstacle:
            
            orientation = gps.correction_orientation(points_parcours, i)

            eviter_obstacle(robot, direction="droite" if orientation > 0 else "gauche")

            orientation = gps.correction_orientation(points_parcours, i)

        else:
            robot.avant()
        time.sleep(0.1)