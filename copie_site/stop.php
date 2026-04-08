<?php
declare(strict_types=1);

require_once __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php?error=method_not_allowed');
    exit();
}

/*
Enregistrer la commande d'arrêt
*/
$stmt = $db->prepare("
    UPDATE commande
    SET action = :action, nom_parcours = NULL
    WHERE id = 1
");

$stmt->bindValue(':action', 'stop', SQLITE3_TEXT);

$result = $stmt->execute();

if ($result === false) {
    header('Location: index.php?error=commande_stop');
    exit();
}

header('Location: index.php?success=robot_stop');
exit();
?>