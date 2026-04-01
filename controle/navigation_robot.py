import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from gps.gps import GPS
from gps.database import Database
class NavigationRobot:

    def __init__(self, robot, gps, db):
        self.robot = robot
        self.gps = gps
        self.db = db
        self.position_robot = self.gps.get_position_robot()
        self.orientation_robot = self.gps.angle_depart(self.robot)

        if self.position_robot is None or self.orientation_robot is None:
            print("Calibration GPS impossible, arrêt.")
            self.robot.arret()
            print("Arrêt du robot")
            raise RuntimeError("Calibration GPS impossible à l'initialisation")
    
    def est_arrive(self, destination, seuil_arrivee=2.0):
        print("Vérification de l'arrivée à la cible")
        if self.position_robot is None:
            print("Erreur GPS")
            return False
        distance = self.gps.distance_2pGPS(self.position_robot, destination)
        return distance < seuil_arrivee
    
    def set_position_robot(self):
        self.position_robot = self.gps.get_position_robot()
            
        if self.position_robot is None:
            print("Erreur GPS")
            self.robot.arret()
            print("Arrêt du robot")
            return
    
    def get_distance_arrivee(self, destination):
        print("Récupération de la distance à la cible")
        if self.position_robot is None:
            print("Erreur GPS")
            self.robot.arret()
            print("Arrêt du robot")
            return None
        return self.gps.distance_2pGPS(self.position_robot, destination)
    
    def get_correction_orientation(self, destination):
        print("Calcul de la correction d'orientation")
        if self.position_robot is None:
            print("Erreur GPS")
            self.robot.arret()
            print("Arrêt du robot")
            return None
        angle_cible = self.gps.get_orientation(self.position_robot, destination)
        if self.orientation_robot is None:
            print("Calibration GPS impossible, arrêt.")
            self.robot.arret()
            print("Arrêt du robot")
            return None
        correction = (angle_cible - self.orientation_robot + 360) % 360
        if correction > 180:
            correction -= 360
        return correction
    
    def correction_orientation(self, destination, seuil_correction=10, facteur_rotation=1.55/360):
        correction = self.get_correction_orientation(destination)
        if correction is None or abs(correction) < seuil_correction:
            return
        print("Correction d'orientation nécessaire :", correction)
        if correction > 0:
            print("Tourne à droite")
            self.robot.rotation_horaire()
        else:
            print("Tourne à gauche")
            self.robot.rotation_trigo()
        time.sleep(abs(correction) * facteur_rotation)
        self.robot.arret()
        print("Arrêt du robot")
        return correction
    
    def set_orientation_robot(self, correction):
        if correction is None:
            return
        self.orientation_robot = (self.orientation_robot + correction) % 360

    def obstacle_detecte(self, seuil_obstacle=20):
        print("Vérification de la présence d'obstacles")
        distance_obstacle = self.robot.distance_obstacle()
        if distance_obstacle is not None and distance_obstacle < seuil_obstacle:
            print("Obstacle détecté")
            return True
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
            
            if self.db.stop_demande():
                print("Arrêt du robot demandé depuis le site")
                self.robot.arret()
                print("Arrêt du robot")
                return
            
            distance_arrivee = self.get_distance_arrivee(points[i])

            if distance_arrivee is None:
                print("Erreur lors du calcul de la distance à la cible, nouvelle tentative")
                continue

            # ARRIVEE
            if self.est_arrive(points[i]):
                self.robot.arret()
                print("Arrêt du robot")
                print("Point atteint")
                if i < len(points)-1:
                    print("Passage au point suivant")
                    i += 1
                    continue
                else:
                    print("Parcours terminé")
                    fin = True
                    self.db.stop_robot_bdd()
                    return

            # ORIENTATION
            correction = self.correction_orientation(points[i])
            if correction is None:
                self.robot.arret()
                return
#            self.set_orientation_robot(correction)              A REVOIR si on ne prend pas en compte les imprécisions du GPS (voir calcul_orientation_deplacement)

            # OBSTACLE
            if self.obstacle_detecte():
                self.eviter_obstacle(direction="droite" if correction > 0 else "gauche")
                continue

            position1 = self.position_robot
            print("Avance vers la cible ")
            self.robot.avant()
            time.sleep(1)
            self.robot.arret()
            position2 = self.gps.get_position_robot()
            if position2 is not None:
                nouvelle_orientation = self.gps.calcul_orientation_deplacement(position1, position2)
                if nouvelle_orientation is not None:
                    self.orientation_robot = nouvelle_orientation
                    self.position_robot = position2