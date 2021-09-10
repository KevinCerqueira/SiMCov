<?php
include_once('auth.php');
include_once('ClientController.php');

$get = isset($_GET) ? $_GET : null;
$post = isset($POST) ? $POST : null;

if(!empty($_GET))