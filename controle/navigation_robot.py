import time

def eviter_obstacle(robot):
    robot.arret()
    time.sleep(0.5)

    robot.arriere()
    time.sleep(1)

    robot.droite()
    time.sleep(0.5)

    robot.avant()
    time.sleep(1)

def calcul_erreur_angle(angle_cible, angle_actuel):
    diff = angle_cible - angle_actuel
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
    return diff

def orienter_vers_cible(robot, get_angle_cible, get_angle_actuel, seuil_angle=10):
    while True:
        angle_cible = get_angle_cible()
        angle_actuel = get_angle_actuel()
        angle_diff = calcul_erreur_angle(angle_cible, angle_actuel)

        if abs(angle_diff) < seuil_angle:
            robot.arret()
            break
        elif angle_diff > 0:
            robot.droite()
        else:
            robot.gauche()
        time.sleep(0.1)

def navigation(robot, get_angle_cible, get_distance_cible, get_angle_actuel, seuil_distance=10):
    orienter_vers_cible(robot, get_angle_cible, get_angle_actuel, seuil_angle=10)
    distance_cible= get_distance_cible()
    distance_arrivee = distance_cible

    while True: 
        if robot.distance_obstacle() < distance_arrivee:
            robot.arret()
            print("Le robot est arrivé à destination !")
            break
        if robot.distance_obstacle() < 20:  # S
            eviter_obstacle(robot)
            continue

        if get_distance_cible() < distance_arrivee:
            robot.arret()
            print("Arrivé à destination")
            break

        angle_cible = get_angle_cible()
        angle_actuel = get_angle_actuel()
        angle_diff = (angle_cible - angle_actuel)
        
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360

        if abs(angle_diff) < seuil_angle
            robot.avant()
        elif angle_diff > 0:
            robot.droite()
        else:
            robot.gauche()
        time.sleep(0.1)

