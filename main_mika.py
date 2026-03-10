import serial
import serial.tools.list_ports
from gps.gps import GPS
from gps.database import lire_destination
import time

if __name__ == '__main__':
    
    gps = GPS()
    gps.port()
    gps.calibration()
    
    ordre = 1
    seuil = 2.0
    
    while True:
        trame = gps_serial.readline().decode("ascii", errors="ignore").strip()
        if not trame.startswith("$GPGGA"):
            continue
        #print(trame)
        print(gps.extraire_position_GPGGA(trame))
        
        position = gps.extraire_position_GPGGA(trame)
        if position is None:
            print("Position GPS invalide")
            continue
        #print("Position actuelle :", position)
        
        destination = lire_destination("test", ordre)
        #print("Destination :", destination)
        if destination is None:
            print("Parcours terminé")
            break
        
        orientation_voulue = gps.orientation(position, destination)
        #print("Orientation cible : ", round(orientation_voulue, 2), "°")
        
        distance_reste = gps.distance_2pGPS(position, destination)
        #print("Distance restante :", round(distance_reste, 2), "m")
                
        # Vérifier si le point est atteint
        if distance_reste < seuil:
            print("Point atteint")
            ordre += 1