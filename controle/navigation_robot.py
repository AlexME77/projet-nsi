import time

distance_arrivee=1.5
distance_min=10
seuil_angle=5

def eviter_obstacle(robot):
    robot.arret()
    time.sleep(1)
    robot.arriere()
    time.sleep(1)
    robot.droite()
    time.sleep(1)
    robot.avant()
    time.sleep(1)

def navigation(robot, get_angle_cible, get_distance_cible, get_angle_actuel):
    while True:
        
        distance_obstacle = robot.distance_obstacle()
        if distance_obstacle < distance_min:
            eviter_obstacle(robot)
            continue

        distance_cible = get_distance_cible()
        if distance_cible < distance_arrivee:
            robot.stop()
            print("Arrivé à destination")
            break

        angle_cible = get_angle_cible()
        angle_actuel = get_angle_actuel()
        angle_diff = (angle_cible - angle_actuel)
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360

        if abs(angle_diff) < seuil_angle:
            robot.avant()
        elif abs(angle_diff) > 0:
            robot.droite(min(angle_diff, 30))
            time.sleep(0.2)
        elif abs(angle_diff) < 0:
            robot.gauche()
            time.sleep(0.2)
        time.sleep(0.1)

