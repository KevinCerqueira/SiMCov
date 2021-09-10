<?php
if (isset($_POST['nome']) && isset($_POST['idade']) && isset($_POST['sexo'])) {
	session_start();
	include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
	$client = new ClientController();
	$response = $client->registerPatient($_POST['nome'], $_POST['idade'], $_POST['sexo']);
	echo json_encode($response);
	die();
}
