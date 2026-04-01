<?php
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['nom_parcours'])) {
$nom_parcours = trim($_POST['nom_parcours']);

if ($nom_parcours !== '') {
$stmt = $pdo->prepare("UPDATE commande SET action = 'start', nom_parcours = :nom WHERE id = 1");
$stmt->execute([':nom' => $nom_parcours]);

// lancer le script python
exec("pgrep -f 'main.py' > /dev/null || sudo python3 /home/pi/Desktop/PROJET/main.py > /tmp/main_python.log 2>&1 &");

header("Location: index.php");
exit;
}
}
?>