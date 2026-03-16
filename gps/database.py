import sqlite3

def coord_destination(nom_parcours):
    """
    Récupère les coordonnées GPS (latitude, longitude)
    d'un point du parcours depuis la base de données
    """
    conn = sqlite3.connect("gps/parcours.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT latitude, longitude FROM points WHERE nom_parcours=? ORDER BY ordre",
        (nom_parcours,)
    )
    resultat = cursor.fetchall()
    conn.close()

    if len(resultat) == 0: 
        raise ValueError(f"Aucun parcours '{nom_parcours}'")
    
    print(resultat)
    return resultat  # (latitude, longitude)

if __name__ == '__main__':
    coord_destination('test')