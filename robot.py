from motor.Motor_Driver import Motor
import time
from capteurs.ultrason import CapteurUltrason

class Robot:

    def __init__(self):
        self.motor = Motor()
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
        return self.capteur_ultrason.mesurer_distance()

if __name__ == '__main__':
    robot = Robot()
    while True:
        print(robot.distance_obstacle())
#    test = Robot()
#    test.set_settings(100)
#    test.avant()
#    time.sleep(2)
#    test.arriere()
#    time.sleep(2)
#    test.rotation_horaire()
#    time.sleep(2)
#    test.rotation_trigo()
#    time.sleep(2)
#    test.arret()
