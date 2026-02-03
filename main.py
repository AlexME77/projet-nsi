import serial
import serial.tools.list_ports
from gps import (extraire_position_GPGGA, calculer_orientation_voulue, calculer_correction)
from database import lire_destination

if __name__ == '__main__':
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
        if not trame.startswith("$GPGGA"):
            continue
        print(trame)
        
        position = extraire_position_GPGGA(trame)
        if position is None:
            print("Position GPS invalide")
            continue
        #print("Position actuelle :", position)
        
        destination = lire_destination("parcours_1", ordre)
        if destination is None:
            print("Aucune destination pour cet ordre")
            continue
        #print(f"Destination (ordre {ordre}) :", destination)
        print("Parcours terminé")
        break
        
        angle_voulu = calculer_orientation_voulue(position, destination)
        #print("Orientation à suivre : ", angle_voulu)
                
        # Vérifier si le point est atteint
        if distance(position, destination) < seuil:
            print("Point atteint")
            ordre += 1