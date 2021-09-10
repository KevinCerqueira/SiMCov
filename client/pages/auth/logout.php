<?php
session_start();
if (isset($_SESSION['auth'])) {
	unset($_SESSION['auth']);
}
// echo 'Location: localhost/SiMCov/client/pages/auth/login.php';
header('Location: login.php');
exit;
