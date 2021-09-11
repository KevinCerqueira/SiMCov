<?php
session_start();
if(!isset($_SESSION['auth'])){
	header('Location: ' . $_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/pages/auth/login.php');
	exit;
}
