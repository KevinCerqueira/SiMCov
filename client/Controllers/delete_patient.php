<?php
session_start();
define('MYPATH', '../');
include_once(MYPATH . 'auth.php');
if (isset($_POST['id'])) {
	include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
	$client = new ClientController();
	$response = $client->deletePatient($_POST['id']);
	echo json_encode($response);
}
