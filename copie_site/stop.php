<?php
include("db.php");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $stmt = $db->prepare("UPDATE commande SET action = :action WHERE id = 1");
    $stmt->bindValue(":action", "stop", SQLITE3_TEXT);
    $stmt->execute();
}

header("Location: index.php");
exit();
?>