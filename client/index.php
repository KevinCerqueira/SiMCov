<?php
include_once('auth.php');
include_once('ClientController.php');

$client = new ClientController();
$client->connect();
$list = $client->send('GET', '/get/list/priority');
// var_dump($list);
foreach($list->data->high as $pat){
	foreach($pat as $p)
		$p->nome;
}
// echo var_dump($client->status());
// var_dump($client->send('GET', '/'));exit;
