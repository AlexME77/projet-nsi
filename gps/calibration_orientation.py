from gps import GPS
from moteur import avancer, arreter
import time

print("Calibration orientation...")

position1 = None
while position1 is None:
    position1 = lire_position_GPS()

avancer(0.5)
time.sleep(0.5)
arreter()

position2 = None
while position2 is None:
    position2 = lire_position_GPS()

orientation_depart = GPS.orientation(position1, position2)
print("Orientation de départ :", orientation_depart)
