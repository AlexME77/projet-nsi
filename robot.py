from motor.Motor_Driver import Motor
import time
from capteurs.distance import CapteurUltrason

class Robot:

    def __init__(self, vitesse = 100):
        self.motor.Setting(0.01, vitesse)
        self.capteur_ultrason = CapteurUltrason()

    def avant(self):
        self.motor.Go_1()
        self.motor.Go_2()

    def arriere(self):
        self.motor.Back_1()
        self.motor.Back_2()

    def arret(self):
        self.motor.Stop()

    def droite(self):
        self.motor.Stop()
        self.motor.Go_1()

    def gauche(self):
        self.motor.Stop()
        self.motor.Go_2()

    def rotation_horaire(self):
        self.motor.Go_1()
        self.motor.Back_2()

    def rotation_trigo(self):
        self.motor.Back_1()
        self.motor.Go_2()
        
    def set_settings(self, vitesse):
        self.motor.Setting(0.01, vitesse)

    def distance_obstacle(self):
        distance = self.capteur_ultrason.mesurer_distance()
        if distance is None or distance <= 0:
            return None
        return distance

    def cleanup(self):
        print("Arrêt des PWM")
        self.motor.OUT_1.stop()
        self.motor.OUT_2.stop()
        self.motor.OUT_3.stop()
        self.motor.OUT_4.stop()
