<?php
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['nom_parcours'])) {
    $nom_parcours = trim($_POST['nom_parcours']);

    $stmt = $db->prepare("UPDATE commande SET action = 'start', nom_parcours = :nom WHERE id = 1");
    $stmt->bindValue(':nom', $nom_parcours, SQLITE3_TEXT);
    $stmt->execute();

    exec("pgrep -f 'main.py' > /dev/null || sudo python3 /home/pi/Desktop/PROJET/main.py > /tmp/main_python.log 2>&1 &");
}

header("Location: index.php");
exit();
?>