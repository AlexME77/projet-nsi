<?php
/**
 * Fichier : db.php
 * Rôle : Gère la connexion à la base de données SQLite.
 * Il crée le fichier de la base de donné et les tables automatiquement au premier lancement.
 */

// On définit le chemin où sera sauvegardée la base de données
$dbPath = '/var/www/html/database/parcours.db';
$dbDir  = dirname($dbPath); // Récupère juste le nom du dossier ("database")

// Crée le dossier s'il n'existe pas encore pour éviter que ça plante
if (!is_dir($dbDir)) {
    mkdir($dbDir, 0775, true);
}

// Connexion à la base SQLite
$db = new SQLite3($dbPath);

/**
 * Création de la table 'points'
 * Elle stocke le nom du parcours et les coordonnées GPS dans l'ordre.
 */
$db->exec("
    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_parcours TEXT,
        ordre INTEGER,
        latitude REAL,
        longitude REAL
    )
");

/**
 * Création de la table 'commande'
 * Elle sert à communiquer avec le robot en Python (action = start ou stop).
 */
$db->exec("
    CREATE TABLE IF NOT EXISTS commande (
        id INTEGER PRIMARY KEY,
        action TEXT,
        nom_parcours TEXT
    )
");

/**
 * Initialisation de la commande
 * On vérifie si la ligne de commande existe déjà pour le robot.
 */
$result = $db->query("SELECT COUNT(*) AS nb FROM commande");
$row = $result->fetchArray();

// Si la table est vide (nb == 0), on ajoute une ligne par défaut en mode 'idle' (repos)
if ($row['nb'] == 0) {
    $db->exec("INSERT INTO commande (id, action, nom_parcours) VALUES (1, 'idle', '')");
}
?>