import sqlite3
class Database:
    """
    Gère les interactions avec la base de données SQLite pour la gestion 
    des parcours et des commandes du robot.
    """
    
    def __init__(self, database_path="/var/www/html/database/parcours.db"):
        """
        Initialise la connexion à la base de données.
        
        paramètre database_path : Chemin absolu vers le fichier de base de données .db
        """
        print("Initialisation de la base de données")
        self.path = database_path

    def _connect(self):
        """
        Crée une connexion à la base de données.
        """
        return sqlite3.connect(self.path, timeout=5)

    def get_commande(self):
        """
        Récupère la commande actuelle (action et nom du parcours) depuis la table 'commande'.
        
        return : Dictionnaire contenant 'action' et 'nom_parcours', ou None si vide.
        """
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT action, nom_parcours FROM commande WHERE id = 1")
        row = cur.fetchone()
        conn.close()

        if row is None:
            print("Aucune commande trouvée")
            return None

        return {
            "action": row[0],
            "nom_parcours": row[1]
        }

    def set_commande(self, action, nom_parcours=None):
        """
        Met à jour l'action et le parcours en cours dans la base de données.
        
        paramètre action : L'action à effectuer (ex: 'start', 'stop', 'pause').
        paramètre nom_parcours : Le nom du parcours associé (optionnel).
        """
        print(f"Changement de commande : action={action}, nom_parcours={nom_parcours}")
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE commande SET action = ?, nom_parcours = ? WHERE id = 1",
            (action, nom_parcours)
        )
        conn.commit()
        conn.close()

    def get_points_parcours(self, nom_parcours):
        """
        Récupère la liste des coordonnées (lat, lon) d'un parcours spécifique, triée par ordre.
        
        paramètre nom_parcours : Le nom du parcours à récupérer.
        return : Liste de tuples (latitude, longitude).
        raise ValueError : Si le nom est vide ou si aucun point n'est trouvé.
        """
        print(f"Récupération des points du parcours '{nom_parcours}'")
        if not nom_parcours:
            raise ValueError("Nom de parcours vide")

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT latitude, longitude
            FROM points
            WHERE nom_parcours = ?
            ORDER BY ordre
            """,
            (nom_parcours,)
        )
        points = cur.fetchall()
        conn.close()

        if not points:
            raise ValueError(f"Aucun point trouvé pour le parcours '{nom_parcours}'")

        return points

    def stop_demande(self):
        """
        Vérifie rapidement si la commande actuelle est définie sur 'stop'.
        
        return True si l'arrêt est demandé, False sinon.
        """
        commande = self.get_commande()
        if commande is None:
            return False
        return commande["action"] == "stop"
