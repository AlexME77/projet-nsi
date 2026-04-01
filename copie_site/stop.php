<?php
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $stmt = $db->prepare("UPDATE commande SET action = 'stop' WHERE id = 1");
    $stmt->execute();
    exec("sudo pkill -f 'python3.*main.py'");
}

header("Location: index.php");
exit();
?>