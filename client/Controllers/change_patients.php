<?php
session_start();
include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
$client = new ClientController();
if(isset($_POST['id_patient']) && isset($_POST['updown']) && isset($_POST['attribute'])){
	$id_patient = $_POST['id_patient'];
	$updown = intval($_POST['updown']);
	$attr = $_POST['attribute'];
	$client->updateAttributeOne($id_patient, $attr, $updown);
}
