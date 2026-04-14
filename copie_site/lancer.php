<?php
include("db.php");

if (isset($_POST['nom_parcours'])) {
    $nomParcours = $_POST['nom_parcours'];

    if ($nomParcours == '') {
        header('Location: index.php?error=nom_parcours_vide');
        exit();
    }

    /*
    Vérifier que le parcours existe vraiment dans la table points
    */
    $requeteCheck = "SELECT COUNT(*) AS total FROM points WHERE nom_parcours = '$nomParcours'";
    $resultCheck = $db->query($requeteCheck);

    if (!$resultCheck) {
        header('Location: index.php?error=verification_parcours');
        exit();
    }

    $row = $resultCheck->fetchArray();

    if ($row['total'] == 0) {
        header('Location: index.php?error=parcours_introuvable');
        exit();
    }

    /*
    Enregistrer la commande de démarrage
    */
    $requeteUpdate = "UPDATE commande SET action = 'start', nom_parcours = '$nomParcours' WHERE id = 1";
    $resultUpdate = $db->exec($requeteUpdate);

    if (!$resultUpdate) {
        header('Location: index.php?error=commande_start');
        exit();
    }

    header('Location: index.php?success=robot_start');
    exit();

} else {
    header('Location: index.php?error=method_not_allowed');
    exit();
}
?>