from motor.Motor_Driver import Motor
class robot:

    def __init__(self):
        self.motor = Motor()
        self.motor.settings(0.01, 60)

    def avant(self, vitesse):
        self.motor.Go_1()
        self.motor.Go_2()

    def arriere(self, vitesse):
        self.motor.Back_1()
        self.motor.Back_2()

    def arret(self):
        self.motor.Stop()

    def droite(self, vitesse):
        self.motor.Stop()
        self.motor.Go_1()

    def gauche(self, vitesse):
        self.motor.Stop()
        self.motor.Go_2()

    def rotation_horaire(self):
        self.motor.Go_1()
        self.motor.Back_2()

    def rotation_trigo(self, angle):
        self.motor.Back_1()
        self.motor.Go_2()