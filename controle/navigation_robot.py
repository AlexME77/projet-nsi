import time
class NavigationRobot:

    def __init__(self, robot, gps, db):
        self.robot = robot
        self.gps = gps
        self.db = db
        self.position_robot = self.gps.get_position_robot()
        self.orientation_robot = self.gps.angle_depart(self.robot)

        if self.position_robot is None or self.orientation_robot is None:
            self.robot.arret()
            raise RuntimeError("Calibration GPS impossible à l'initialisation")
    
    def set_position_robot(self):
        print("Mise à jour de la position du robot")
        self.position_robot = self.gps.get_position_robot()
    
    def get_distance_arrivee(self, destination):
        print("Récupération de la distance à la cible")
        if self.position_robot is None:
            return None
        return self.gps.distance_2pGPS(self.position_robot, destination)
    
    def get_correction_orientation(self, destination):
        print("Calcul de la correction d'orientation")
        if self.position_robot is None:
            return None
        angle_cible = self.gps.get_orientation(self.position_robot, destination)
        correction = (angle_cible - self.orientation_robot + 360) % 360
        if correction > 180:
            correction -= 360
        return correction
    
    def correction_orientation(self, destination, seuil_correction=10, facteur_rotation=1.55/360):
        correction = self.get_correction_orientation(destination)
        if correction is None:
            print("Erreur de calcul de la correction d'orientation")
            return None
        if abs(correction) < seuil_correction:
            print("Correction d'orientation négligeable, pas de rotation nécessaire")
            return 0
        print("Correction d'orientation nécessaire :", correction)
        if correction > 0:
            self.robot.rotation_horaire()
        else:
            self.robot.rotation_trigo()
        time.sleep(abs(correction) * facteur_rotation)
        self.robot.arret()
        return correction
    
    def set_orientation_robot(self, correction):
        print("Mise à jour de l'orientation du robot")
        self.orientation_robot = (self.orientation_robot + correction) % 360

    def obstacle_detecte(self, seuil_obstacle=20):
        print("Vérification de la présence d'obstacles")
        distance_obstacle = self.robot.distance_obstacle()
        if distance_obstacle is not None and distance_obstacle < seuil_obstacle:
            print("Obstacle détecté")
            return True
        print("Aucun obstacle détecté")
        return False

    def eviter_obstacle(self, direction="droite"):
        print("Début de l'évitement d'obstacle")
        
        self.robot.arret()
        time.sleep(0.5)

        self.robot.arriere()
        time.sleep(0.7)

        if direction == "droite":
            self.robot.droite()
        else:
            self.robot.gauche()
        time.sleep(0.7)

        self.robot.avant()
        time.sleep(1)

        self.robot.arret()

        print("Fin de l'évitement d'obstacle")
        
    def navigation(self, points):

        i=0
        fin = False

        while not fin:
            
            # ARRÊT DEMANDÉ
            if self.db.stop_demande():
                print("Arrêt du robot demandé depuis le site")
                self.robot.arret()
                return
            
            # POSITION
            self.set_position_robot()
            if self.position_robot is None:
                print("Erreur GPS, nouvelle tentative de récupération de la position du robot")
                continue

            # ARRIVEE
            distance_arrivee = self.get_distance_arrivee(points[i])
            if distance_arrivee is None:
                print("Erreur lors du calcul de la distance à la cible, nouvelle tentative")
                continue
            if distance_arrivee < 2.0:
                self.robot.arret()
                print("Point atteint")
                if i < len(points)-1:
                    print("Passage au point suivant")
                    i += 1
                    continue
                else:
                    print("Parcours terminé")
                    fin = True
                    continue

            # ORIENTATION
            correction = self.correction_orientation(points[i])
            if correction is None:
                continue
            self.set_orientation_robot(correction)

            # OBSTACLE
            if self.obstacle_detecte():
                self.eviter_obstacle(direction="droite" if correction > 0 else "gauche")
                continue

            # DÉPLACEMENT
            position1 = self.position_robot
            print("Rien d'anormal détecté, déplacement vers la cible")
            self.robot.avant()
            time.sleep(1)
            self.robot.arret()
            position2 = self.gps.get_position_robot()
            if position2 is None:
                print("Erreur GPS, nouvelle tentative de récupération de la position du robot")
                continue
            nouvelle_orientation = self.gps.calcul_orientation_deplacement(position1, position2)
            if nouvelle_orientation is None:
                print("Erreur GPS, nouvelle tentative de récupération de l'orientation du robot")
                continue

            self.orientation_robot = nouvelle_orientation
            self.position_robot = position2

        print("Navigation terminée.")
        return