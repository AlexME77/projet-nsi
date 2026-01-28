import serial
from gps import (extraire_position_GPRMC, calculer_orientation_voulue, calculer_correction)
from database import lire_destination

if __name__ == '__main__':
    gps = serial.Serial("COM4", 4800, timeout=1)
    ordre = 1
    seuil = 0.00005
    while True:
        trame = gps.readline().decode("ascii", errors="ignore").strip()
        if trame.startswith("$GPRMC"):
            position = extraire_position_GPRMC(trame)
            if position is not None:
                destination = lire_destination("parcours_1", ordre)
                if destination is not None:
                    print("Parcours terminé")
                    break
                
                angle_voulu = calculer_orientation_voulue(position, destination)
                
                print(f"Position : {position}")
                print(f"Destination (ordre {ordre}) : {destination}")
                print(f"Orientation à suivre : {angle_voulu:.2f}°")
                
                # Vérifier si le point est atteint
                if distance(position, destination) < seuil:
                    print("Point atteint")
                    ordre += 1
  
