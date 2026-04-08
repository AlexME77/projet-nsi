<?php
declare(strict_types=1);

$dbDirectory = __DIR__ . '/database';
$dbPath = $dbDirectory . '/parcours.db';

if (!is_dir($dbDirectory)) {
    mkdir($dbDirectory, 0775, true);
}

$db = new SQLite3($dbPath);
$db->busyTimeout(5000);
$db->exec('PRAGMA foreign_keys = ON;');

/*
Table des points qui se créé si elle n'existe pas
*/
$db->exec("
    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_parcours TEXT NOT NULL CHECK (length(trim(nom_parcours)) > 0),
        ordre INTEGER NOT NULL CHECK (ordre > 0),
        latitude REAL NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
        longitude REAL NOT NULL CHECK (longitude >= -180 AND longitude <= 180)
    )
");

$db->exec("
    CREATE INDEX IF NOT EXISTS idx_parcours_ordre
    ON points(nom_parcours, ordre)
");

$db->exec("
    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_point
    ON points(nom_parcours, ordre)
");

/*
Table de commande robot
*/
$db->exec("
    CREATE TABLE IF NOT EXISTS commande (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        action TEXT NOT NULL CHECK (action IN ('idle', 'start', 'stop')),
        nom_parcours TEXT
    )
");

$db->exec("
    INSERT OR IGNORE INTO commande (id, action, nom_parcours)
    VALUES (1, 'idle', NULL)
");
?>