<?php
session_start();
if(!isset($_SESSION['auth'])){
	header('Location: ' . MYPATH . 'pages/auth/login.php');
	exit;
}
