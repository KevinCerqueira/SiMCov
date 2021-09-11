<?php
include_once(MYPATH . 'auth.php');
include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
$client = new ClientController();
$search_patients = $client->getAll();
?>