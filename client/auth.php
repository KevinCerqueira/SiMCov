<?php
session_start();
if(!isset($_SESSION['auth'])){
	header('Location: pages/auth/login.php');
	exit;
}
