import serial
import serial.tools.list_ports
from gps import GPS
from database import lire_destination

if __name__ == '__main__':
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Aucun port série détecté")
        exit()
    port = ports[0].device
    print("Port GPS détecté :", port)
    gps_serial = serial.Serial(port, 4800, timeout=1)
    
    ordre = 1
    seuil = 0.00005
    
    while True:
        trame = gps_serial.readline().decode("ascii", errors="ignore").strip()
        if not trame.startswith("$GPGGA"):
            continue
        print(trame)
        
        position = GPS.extraire_position_GPGGA(trame)
        if position is None:
            print("Position GPS invalide")
            continue
        #print("Position actuelle :", position)
        
        destination = lire_destination("parcours_1", ordre)
        #print("Destination :", destination)
        if destination is None:
            print("Parcours terminé")
            break
        
        angle_voulu = GPS.orientation(position, destination)
        #print("Orientation à suivre : ", angle_voulu)
        
        distance = GPS.distance_2pGPS(position, destination)
        #print("Distance :", round(distance, 2), "m")
                
        # Vérifier si le point est atteint
        if distance < seuil:
            print("Point atteint")
            ordre += 1