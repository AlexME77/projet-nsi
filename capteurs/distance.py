
# Import des librairies GPIO et time (temps et conversion) #
import RPi.GPIO as GPIO
import time
 
# Module GPIO: BOARD ou BCM (numérotation comme la sérigraphie de la carte ou comme le chip) #
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)

TRIG = 3
ECHO = 4

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
 
class CapteurUltrason:

    def __init__(self, TRIG=3, ECHO=4):
        self.trig = TRIG
        self.echo = ECHO
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
 
    def mesurer_distance(self):
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
            return None

        duree = end - start
        distance = (duree * 34300) / 2
    
        return distance
 
if __name__ == '__main__':
    capteur = CapteurUltrason()
    while True:
        d = capteur.mesurer_distance()
        print(d)
        time.sleep(0.5)
