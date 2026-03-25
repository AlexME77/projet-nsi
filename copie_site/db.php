<?php

$db = new SQLite3(__DIR__ . "/database/parcours.db");

$db->exec("
    CREATE TABLE IF NOT EXISTS commande (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        action TEXT NOT NULL,
        nom_parcours TEXT
    )
");

$db->exec("
    INSERT OR IGNORE INTO commande (id, action, nom_parcours)
    VALUES (1, 'idle', NULL)
");

?>