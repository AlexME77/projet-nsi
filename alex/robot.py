from motor.Motor_Driver import Motor
import time

class robot:

    def __init__(self):
        self.motor = Motor()

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

if __name__ == '__main__':
    test = robot()
    test.avant()
    time.sleep(2)
    test.arret()
