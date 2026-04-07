
# Import des librairies GPIO et time (temps et conversion) #
import RPi.GPIO as GPIO
import time
 
# Module GPIO: BOARD ou BCM (numérotation comme la sérigraphie de la carte ou comme le chip) #
GPIO.setwarnings(False) 
 
class CapteurUltrason:

    def __init__(self, trig=2, echo=3):
        self.trig = trig
        self.echo = echo
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
 
    def mesurer_distance(self):
        # Mise à l'état haut de la broche Trigger #
        GPIO.output(self.trig, True)
    
        # Mise à l'état bas de la broche Trigger aprés 10 µS #
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # Enregistrement du temps de départ des ultrasons #
        timeout = time.time() + 0.02  # 20 ms max
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
            if StartTime > timeout:
                return None  # erreur
    
        # Enregistrement du temps d'arrivés des ultrasons #
        timeout = time.time() + 0.02
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
            if StopTime > timeout:
                return None  # erreur
    
        # Calcul de la durée de l'aller-retour des US #
        TimeElapsed = StopTime - StartTime
        # On multiplue la durée par la vitesse du son: 34300 cm/s #
        # et on divise par deux car il s'agit d'un aller et retour. #
        distance = (TimeElapsed * 34300) / 2
    
        return distance
 
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    capteur = CapteurUltrason()
    try:
        while True:
            dist = capteur.mesurer_distance()
            if dist is None:
                print("Erreur de mesure (timeout)")
            else:
                print("Distance mesurée = ", dist)
            time.sleep(1)
 
        # On reset le programme via CTRL+C #
    except KeyboardInterrupt:
        print("Mesure stoppée")
        GPIO.cleanup()
