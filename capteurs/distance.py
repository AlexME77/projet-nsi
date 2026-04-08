
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
class CapteurUltrason:

    def __init__(self, TRIG=3, ECHO=4):
        print("Initialisation du capteur ultrason")
        self.trig = TRIG
        self.echo = ECHO
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
 
    def mesurer_distance(self):
        print("Mesure de la distance à l'obstacle")
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start = None
        end = None
    
        timeout = time.time() + 0.02 
        while GPIO.input(self.echo) == 0:
            if time.time() > timeout:
                return None 
            start = time.time()
    
        timeout = time.time() + 0.02
        while GPIO.input(self.echo) == 1:
            if time.time() > timeout:
                return None 
            end = time.time()
    
        if start is None or end is None:
            print("Erreur de mesure capteur ultrason : signal non reçu")
            return None

        duree = end - start
        distance = (duree * 34300) / 2
    
        return distance
 
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    capteur = CapteurUltrason()
    while True:
        d = capteur.mesurer_distance()
        print(d)
        time.sleep(0.5)
