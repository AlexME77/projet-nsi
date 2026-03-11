import time
from gps.gps import GPS
from gps.database import lire_destination

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
def navigation(robot, parcours, seuil_obstacle=20, seuil_arrivee=2.0):
    gps = GPS()
    gps.port()
    gps.calibration()

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
            
            orientation = gps.orientation(gps.lire_position_GPS(), lire_destination(parcours, ordre=i))
# Pour tout ce qui est orientation pour éviter de faire des tours pour rien il faudrait faire une fonction qui calcule le bon anglais si et renvoie droite ou gauche et la valeur de l'angle mais seulement de -180 à 180 pour éviter de faire des tours de 360° ou plus
            eviter_obstacle(robot, direction="droite" if orientation < 180 else "gauche")

            orientation = gps.orientation(gps.lire_position_GPS(), lire_destination(parcours, ordre=i))

            if orientation < 180:
                robot.rotation_trigo()

            else:
                robot.rotation_horaire()
            
            time.sleep(orientation/30)  # Ajuster le temps de rotation en fonction de l'orientation (trouver la bonne valeur et faire attention à la vitesse garder toujours la même)
# On peut même faire une fonction ou une relation qui calcule le temps de rotation en fonction de l'orientation et de la vitesse du robot

        else:
            robot.avant()
        time.sleep(0.1)