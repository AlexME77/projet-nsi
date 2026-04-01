import sqlite3

DB_PATH = "/var/www/html/robot/database/parcours.db"

def coord_destination():
    """
    Récupère les coordonnées GPS (latitude, longitude)
    d'un point du parcours depuis la base de données
    """
    print("Connexion à la base de données")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Récupération du nom du parcours")
    cursor.execute(
    "SELECT nom_parcours FROM commande WHERE action=?",
    ("start",)
    )
    parcours = cursor.fetchone()
   
    if parcours is None:
        raise ValueError("Aucune commande 'start' trouvée")
    
    nom_parcours = parcours[0]
    print("Récupération du nom du parcours terminée : ", nom_parcours)


    print("Récupération des coordonnées GPS du parcours")
    cursor.execute(
        "SELECT latitude, longitude FROM points WHERE nom_parcours=? ORDER BY ordre",
        (nom_parcours,)
    )
    points = cursor.fetchall()
    conn.close()
    print("Déconnexion de la base de données, récupération des coordonnées GPS terminée")

    print("Vérification si la base de données est vide")
    if len(points) == 0: 
        raise ValueError(f"Aucun points pour parcours '{nom_parcours}'")
    
    print(f"Les points du parcours sont : {points}")
    return points

def get_commande():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT action FROM commande WHERE id = 1;")
    commande = cur.fetchone()
    conn.close()

    if commande:
        return commande
    return None


def stop_demande():
    action, _ = get_commande()
    return action == "stop"

def stop_robot_bdd():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE commande SET action = ? WHERE id=1", ("stop"))
    conn.close()

if __name__ == '__main__':
    coord_destination()
