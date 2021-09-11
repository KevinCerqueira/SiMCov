<?php
session_start();
if (isset($_SESSION['auth'])) {
	header('Location: ' . MYPATH . 'index.php');
	exit;
}
if (isset($_POST['username']) && isset($_POST['password'])) {
	include_once('ClientController.php');
	$username = $_POST['username'];
	$password = $_POST['password'];
	$client = new ClientController();
	$response = $client->register($username, $password);
	echo json_encode($response);
	die();
}
