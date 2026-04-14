<?php
include("db.php");

$requete = "UPDATE commande SET action = 'stop', nom_parcours = NULL WHERE id = 1";
$result = $db->exec($requete);

if (!$result) {
    header('Location: index.php?error=commande_stop');
    exit();
}

header('Location: index.php?success=robot_stop');
exit();
?>