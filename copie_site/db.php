<?php
// On crée la Base de donné
$dbPath = '/var/www/html/database/parcours.db';
$dbDir  = dirname($dbPath);
if (!is_dir($dbDir)) {
    mkdir($dbDir, 0775, true);
}
$db = new SQLite3($dbPath);

/*
Table des points
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

/*
Table de commande robot
*/
$db->exec("
    CREATE TABLE IF NOT EXISTS commande (
        id INTEGER PRIMARY KEY,
        action TEXT,
        nom_parcours TEXT
    )
");

/*
On vérifie si la ligne de commande existe déjà, sinon on l'ajoute.
*/
$result = $db->query("SELECT COUNT(*) AS nb FROM commande");
$row = $result->fetchArray();

if ($row['nb'] == 0) {
    $db->exec("INSERT INTO commande (id, action, nom_parcours) VALUES (1, 'idle', '')");
}
?>