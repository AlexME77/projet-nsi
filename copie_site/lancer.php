<?php
declare(strict_types=1);

require_once __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php?error=method_not_allowed');
    exit();
}

$nomParcours = trim($_POST['nom_parcours'] ?? '');

if ($nomParcours === '') {
    header('Location: index.php?error=nom_parcours_vide');
    exit();
}

/*
Vérifier que le parcours existe vraiment dans la table points
*/
$stmtCheck = $db->prepare("
    SELECT COUNT(*) AS total
    FROM points
    WHERE nom_parcours = :nom
");

$stmtCheck->bindValue(':nom', $nomParcours, SQLITE3_TEXT);
$resultCheck = $stmtCheck->execute();

if ($resultCheck === false) {
    header('Location: index.php?error=verification_parcours');
    exit();
}

$row = $resultCheck->fetchArray(SQLITE3_ASSOC);
$resultCheck->finalize();

if ((int)($row['total'] ?? 0) === 0) {
    header('Location: index.php?error=parcours_introuvable');
    exit();
}

/*
Enregistrer la commande de démarrage
*/
$stmtUpdate = $db->prepare("
    UPDATE commande
    SET action = :action, nom_parcours = :nom
    WHERE id = 1
");

$stmtUpdate->bindValue(':action', 'start', SQLITE3_TEXT);
$stmtUpdate->bindValue(':nom', $nomParcours, SQLITE3_TEXT);

$resultUpdate = $stmtUpdate->execute();

if ($resultUpdate === false) {
    header('Location: index.php?error=commande_start');
    exit();
}

header('Location: index.php?success=robot_start');
exit();
?>