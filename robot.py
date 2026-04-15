# Réalisé par : Alexandre Mai--Emery

from Motor_Driver import Motor
from capteur_ultrason import CapteurUltrason

class Robot:

    def __init__(self, vitesse = 75):
        print("Initialisation du robot")
        self.motor = Motor()
        self.motor.Setting(0.01, vitesse)
        self.capteur_ultrason = CapteurUltrason()

    def avant(self):
        '''
        Fait avancer le robot.
        '''
        print("Avance")
        self.motor.Go_1()
        self.motor.Go_2()

    def arriere(self):
        '''
        Fait reculer le robot.
        '''
        print("Recule")
        self.motor.Back_1()
        self.motor.Back_2()

    def arret(self):
        '''
        Fait s'arrêter le robot.
        '''
        print("Arrêt")
        self.motor.Stop()

    def droite(self):
        '''
        Fait tourner le robot à droite.
        '''
        print("Tourne à droite")
        self.motor.Stop()
        self.motor.Go_1()

    def gauche(self):
        '''
        Fait tourner le robot à gauche.
        '''
        print("Tourne à gauche")
        self.motor.Stop()
        self.motor.Go_2()

    def rotation_horaire(self):
        '''
        Rotation dans le sens horaire
        '''
        print("Rotation horaire")
        self.motor.Go_1()
        self.motor.Back_2()

    def rotation_trigo(self):
        '''
        Rotation dans le sens trigonométrique (antihoraire)
        '''
        print("Rotation trigonométrique (antihoraire)")
        self.motor.Back_1()
        self.motor.Go_2()

    def distance_obstacle(self):
        '''
        Mesure la distance à l'obstacle.
        '''
        print("Mesure de la distance à l'obstacle")
        distance = self.capteur_ultrason.mesurer_distance()
        if distance is None or distance <= 0:
            return None
        return distance

    def cleanup(self):
        '''
        Nettoyage des ressources utilisées par le robot.
        '''
        print("Arrêt des PWM")
        self.motor.OUT_1.stop()
        self.motor.OUT_2.stop()
        self.motor.OUT_3.stop()
        self.motor.OUT_4.stop()