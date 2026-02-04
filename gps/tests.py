import serial
import serial.tools.list_ports
from gps import (extraire_position_GPGGA, calculer_orientation_voulue, calculer_correction)
from database import lire_destination

ports = list(serial.tools.list_ports.comports())
if len(ports) == 0:
    print("Aucun port série détecté")
    exit()
port = ports[0].device
print("Port GPS détecté :", port)
gps = serial.Serial(port, 4800, timeout=1)
ordre = 1
seuil = 0.00005
while True:
    trame = gps.readline().decode("ascii", errors="ignore").strip()
    if trame.startswith("$GPGGA"):
        position = extraire_position_GPGGA(trame)
        if position is None:
            print("Position GPS invalide")
        else:
            destination = lire_destination("parcours_1", ordre)
            if destination is None:
                print("Aucune destination pour cet ordre")
            else:
                print("Parcours terminé")
                break
            
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