import serial
from gps import (extraire_position_GPRMC, calculer_orientation_voulue, calculer_correction)
from database import lire_destination

#gps = serial.Serial("COM4", 4800, timeout=1)
#while True:
#    trame = gps.readline().decode("ascii", errors="ignore").strip()
#    if trame.startswith("$GPRMC"):
#        position_gps_actuelle = extraire_position_GPRMC(trame)
#        if position_gps_actuelle is not None:
#            print("Position actuelle :", position)
            
position = (0.0, 0.0)
destination = (1.0, 0.0)
print(calculer_orientation_voulue(position, destination))
destination = (0.0, 1.0)
print(calculer_orientation_voulue(position, destination))
destination = (-1.0, 0.0)
print(calculer_orientation_voulue(position, destination))
destination = (0.0, -1.0)
print(calculer_orientation_voulue(position, destination))

orientation_actuelle = 0
orientation_voulue = 90
print(calculer_correction(orientation_actuelle, orientation_voulue))
orientation_actuelle = 90
orientation_voulue = 0
print(calculer_correction(orientation_actuelle, orientation_voulue))
orientation_actuelle = 350
orientation_voulue = 10
print(calculer_correction(orientation_actuelle, orientation_voulue))

position = (48.88294, 2.61215) # position GPS réelle
destination = (48.88350, 2.61300) # destination fictive
angle_voulu = calculer_orientation_voulue(position, destination)
print("Orientation à suivre :", angle_voulu)

destination = lire_destination("parcours_1", 1)
print("Destination :", destination)