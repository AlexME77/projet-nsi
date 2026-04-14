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

// Vérifier que le parcours existe dans la base
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

// Mettre à jour la commande dans la base
try {
    $db->exec("BEGIN");
    $stmtUpdate = $db->prepare("
        UPDATE commande
        SET action = :action, nom_parcours = :nom
        WHERE id = 1
    ");
    $stmtUpdate->bindValue(':action', 'start', SQLITE3_TEXT);
    $stmtUpdate->bindValue(':nom', $nomParcours, SQLITE3_TEXT);
    $stmtUpdate->execute();

    // Vérifier que la ligne a bien été modifiée
    if ($db->changes() === 0) {
        $db->exec("ROLLBACK");
        header('Location: index.php?error=commande_start');
        exit();
    }
    $db->exec("COMMIT");
} catch (Exception $e) {
    $db->exec("ROLLBACK");
    header('Location: index.php?error=commande_start');
    exit();
}

// Lancer le programme Python si pas déjà en cours
exec("pgrep -f 'main.py' > /dev/null 2>&1", $out, $running);
if ($running !== 0) {
    exec("sudo python3 /home/pi/Desktop/PROJET/main.py >> /tmp/robot.log 2>&1 &");
}

header('Location: index.php?success=robot_start');
exit();
?>