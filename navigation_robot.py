# Réalisé par : Alexandre Mai--Emery
import time
class NavigationRobot:

    def __init__(self, robot, gps, db):
        self.robot = robot
        self.gps = gps
        self.db = db
        self.orientation_robot = self.gps.angle_depart(self.robot)
        self.position_robot = self.gps.attendre_position()
        
    def set_position_robot(self):
        '''
        Met à jour la position du robot (attribut position_robot) en utilisant la fonction get_position_robot du GPS
        '''
        print("Mise à jour de la position du robot")
        self.position_robot = self.gps.get_position_robot()
    
    def get_distance_arrivee(self, destination):
        '''
        Calcule la distance entre la position actuelle du robot (attribut position_robot) et la destination (en paramètre) en utilisant la fonction distance_2pGPS du GPS
        Retourne la distance en mètres ou None en cas d'erreur de calcul
        '''
        print("Récupération de la distance à la cible")
        if self.position_robot is None:
            return None
        return self.gps.distance_2pGPS(self.position_robot, destination)
    
    def get_correction_orientation(self, destination):
        '''
        Calcule la correction d'orientation nécessaire pour atteindre la destination (en paramètre) en utilisant la fonction get_orientation du GPS
        Retourne la correction d'orientation en degrés (positive pour une rotation horaire, négative pour une rotation trigonométrique) ou None en cas d'erreur de calcul
        '''
        print("Calcul de la correction d'orientation")
        if self.position_robot is None:
            return None
        angle_cible = self.gps.get_orientation(self.position_robot, destination)
        correction = (angle_cible - self.orientation_robot + 360) % 360

        # La correction est ajustée pour être dans l'intervalle [-180, 180] et ne pas faire de rotation inutile
        if correction > 180:
            correction -= 360
        return correction
    
    def correction_orientation(self, destination, seuil_correction=10, facteur_rotation=2.25/360):
        '''
        Corrige l'orientation du robot pour qu'il pointe vers la destination (en paramètre) en utilisant la fonction get_correction_orientation
        Si la correction d'orientation est inférieure au seuil de correction (en degrés, en paramètre), aucune rotation n'est effectuée
        Le facteur de rotation (en secondes par degré, en paramètre) est utilisé pour calculer la durée de la rotation en fonction de la correction d'orientation (nous avons trouver que le robot met environ time.sleep(2.25) pour faire une rotation complète de 360 degrés avec la vitesse du robot à 75)
        '''
        correction = self.get_correction_orientation(destination)
        
        if correction is None:
            print("Erreur de calcul de la correction d'orientation")
            return None
        
        # Vérification si la correction d'orientation est inférieure au seuil de correction pour éviter les rotations inutiles
        if abs(correction) < seuil_correction:
            print("Correction d'orientation négligeable, pas de rotation nécessaire")
            return 0
        print("Correction d'orientation nécessaire :", correction)

        # Rotation du robot dans la direction de la correction d'orientation
        if correction > 0:
            self.robot.rotation_horaire()
        else:
            self.robot.rotation_trigo()

        # Calcul de la durée de la rotation en fonction de la correction d'orientation et du facteur de rotation
        time.sleep(abs(correction) * facteur_rotation)

        self.robot.arret()
        return correction
    
    def set_orientation_robot(self, correction):
        '''
        Met à jour l'orientation du robot (attribut orientation_robot) en utilisant un angle en degré (paramètre correction)
        '''
        print("Mise à jour de l'orientation du robot")
        self.orientation_robot = (self.orientation_robot + correction) % 360

    def obstacle_detecte(self, seuil_obstacle=20):
        '''
        Détecte la présence d'obstacles devant le robot en utilisant la fonction distance_obstacle du robot
        Si la distance à l'obstacle est inférieure au seuil d'obstacle (en centimètres, en paramètre), la fonction retourne True pour indiquer qu'un obstacle est détecté, sinon elle retourne False
        '''
        print("Vérification de la présence d'obstacles")
        distance_obstacle = self.robot.distance_obstacle()
        if distance_obstacle is not None and distance_obstacle < seuil_obstacle:
            print("Obstacle détecté")
            return True
        print("Aucun obstacle détecté")
        return False

    def eviter_obstacle(self, direction="droite"):
        '''
        Effectue une manœuvre d'évitement d'obstacle en reculant, en tournant dans la direction spécifiée (paramètre direction, "droite" ou "gauche") et en avançant à nouveau
        '''
        print("Début de l'évitement d'obstacle")
        
        # Arrêt du robot
        self.robot.arret()
        time.sleep(0.5)

        # Recul du robot
        self.robot.arriere()
        time.sleep(1)

        # Rotation du robot dans la direction spécifiée
        if direction == "droite":
            self.robot.rotation_horaire()
        else:
            self.robot.rotation_trigo()
        time.sleep(1)

        # Robot avance
        self.robot.avant()
        time.sleep(1)

        # Rotation du robot dans la direction inverse pour retrouver son axe
        self.robot.rotation_trigo() if direction == "droite" else self.robot.rotation_horaire()
        time.sleep(1)

        self.robot.arret()
        print("Fin de l'évitement d'obstacle")
        
    def navigation(self, points):
        '''
        Effectue la navigation du robot vers les points du parcours (paramètre points, liste de coordonnées GPS) en utilisant les fonctions précédentes pour mettre à jour la position et l'orientation du robot, calculer la distance à la cible, corriger l'orientation, détecter les obstacles et éviter les obstacles
        La navigation se termine lorsque le robot atteint le dernier point du parcours ou lorsqu'une demande d'arrêt est détectée dans la base de données
        '''

        i=0
        fin = False

        while not fin:
            
            # Arrêt demandé par la base de données
            if self.db.stop_demande():
                print("Arrêt du robot demandé depuis le site")
                self.robot.arret()
                return
            
            # Mise à jour de la position du robot
            self.set_position_robot()
            if self.position_robot is None:
                print("Erreur GPS, nouvelle tentative de récupération de la position du robot")
                continue

            # Calcul de la distance à la cible
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

            # Correction de l'orientation du robot
            correction = self.correction_orientation(points[i])
            if correction is None:
                continue
            self.set_orientation_robot(correction)

            position1 = self.position_robot

            # Détection d'obstacles et évitement si nécessaire
            if self.obstacle_detecte():
                self.eviter_obstacle(direction="droite" if correction >= 0 else "gauche")
                continue

            # Déplacement du robot vers la cible
            print("Rien d'anormal détecté, déplacement vers la cible")
            self.robot.avant()
            time.sleep(1)
            self.robot.arret()
            position2 = self.gps.get_position_robot()
            if position2 is None:
                print("Erreur GPS, nouvelle tentative de récupération de la position du robot")
                continue

            # Mise à jour de l'orientation et de la position du robot après le déplacement
            nouvelle_orientation = self.gps.get_orientation(position1, position2)
            self.orientation_robot = nouvelle_orientation
            self.position_robot = position2

        print("Navigation terminée.")
        return
