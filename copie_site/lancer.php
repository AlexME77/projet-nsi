<?php
include("db.php");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nom_parcours = $_POST["nom_parcours"];

    $stmt = $db->prepare("UPDATE commande SET action = :action, nom_parcours = :nom_parcours WHERE id = 1");
    $stmt->bindValue(":action", "start", SQLITE3_TEXT);
    $stmt->bindValue(":nom_parcours", $nom_parcours, SQLITE3_TEXT);
    $stmt->execute();
    exec("sudo python3 /home/pi/Desktop/PROJET/main.py > /tmp/main_python.log 2>&1 &");
}

header("Location: index.php");
exit();
?>
