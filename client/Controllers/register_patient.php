<?php
/**
 * Componente Curricular: MI Concorrência e Conectividade
 * Autor: Kevin Cerqueira Gomes
 *
 * Declaro que este código foi elaborado por mim de forma individual e
 * não contém nenhum trecho de código de outro colega ou de outro autor,
 * tais como provindos de livros e apostilas, e páginas ou documentos
 * eletrônicos da Internet. Qualquer trecho de código de outra autoria que
 * uma citação para o  não a minha está destacado com  autor e a fonte do
 * código, e estou ciente que estes trechos não serão considerados para fins
 * de avaliação. Alguns trechos do código podem coincidir com de outros
 * colegas pois estes foram discutidos em sessões tutorias.
*/
if (isset($_POST['nome']) && isset($_POST['idade']) && isset($_POST['sexo'])) {
	session_start();
	include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
	$client = new ClientController();
	$response = $client->registerPatient($_POST['nome'], $_POST['idade'], $_POST['sexo']);
	echo json_encode($response);
	die();
}
