<?php
session_start();
define('MYPATH', '../');
include_once(MYPATH . 'auth.php');
include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
$client = new ClientController();
$response = $client->getAll();
echo json_encode($response);
?>