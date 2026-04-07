import sqlite3

class Database():
    
    def __init__(self, database_path="/var/www/html/database/parcours.db"):
        self.path = database_path

    def coord_destination(self):
        """
        Récupère les coordonnées GPS (latitude, longitude)
        d'un point du parcours depuis la base de données
        """
        print("Connexion à la base de données")
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        print("Récupération du nom du parcours")
        cursor.execute(
        "SELECT nom_parcours FROM commande WHERE action=?",
        ("start",)
        )
        parcours = cursor.fetchone()
    
        if parcours is None:
            conn.close()
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

    def get_commande(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("SELECT action FROM commande WHERE id = 1;")
        commande = cur.fetchone()
        conn.close()

        if commande:
            return commande
        return None


    def stop_demande(self):
        commande = self.get_commande()
        if commande is None:
            return False
        return commande[0] == "stop"

    def stop_robot_bdd(self):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("UPDATE commande SET action = ? WHERE id=1", ("stop",))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = Database()
    db.coord_destination()
