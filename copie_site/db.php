<?php
declare(strict_types=1);

$dbDirectory = __DIR__ . '/database';
$dbPath = $dbDirectory . '/parcours.db';

if (!is_dir($dbDirectory)) {
    mkdir($dbDirectory, 0775, true);
}

// S'assurer que la DB est accessible en écriture
if (file_exists($dbPath) && !is_writable($dbPath)) {
    die("Erreur : la base de données n'est pas accessible en écriture. Vérifiez les permissions.");
}

$db = new SQLite3($dbPath);
$db->busyTimeout(5000);
$db->exec('PRAGMA journal_mode=WAL;');   // évite les locks entre PHP et Python
$db->exec('PRAGMA foreign_keys = ON;');

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
    CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_point
    ON points(nom_parcours, ordre)
");

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