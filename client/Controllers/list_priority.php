<?php
session_start();
include_once($_SERVER['DOCUMENT_ROOT'] . '/SiMCov/client/Controllers/ClientController.php');
$client = new ClientController();
$response = $client->getListPriority();
if ($response->success) {
	$high = "<p class='h5 text-white p-1 bg-success'>Sem pacientes para este nível.</p>";
	$medium = $high;
	$normal = $medium;
	$alert = false;
	if (isset($_SESSION['list_priority'])) {
		if ((count($_SESSION['list_priority']->high) != count($response->data->high)))
			$alert = true;
		elseif (isset($_SESSION['list_priority']->high[0]) && isset($response->data->high[0]) && $_SESSION['list_priority']->high[0]->nome != $response->data->high[0]->nome)
			$alert = true;
	}
	$_SESSION['list_priority'] = $response->data;
	foreach ($response->data->high as $index => $patient) {
		if ($index == 0) {
			$high = "";
		}
		$high .= "<div class='mb-2'>";
		$high .= "<p class='bg-danger m-0 text-white fw-bold'>" . $patient->nome . "</p><p class='bg-danger m-0 text-white fw-bold'>" .  $patient->idade . " anos | " . $patient->sexo . "</p>";
		$high .= "<p class='bg-danger m-0 text-white'><label class='fw-bold'>SpO2: " . $patient->saturacao . "%</label>&nbsp;&nbsp;&nbsp;" .
			" <i class='fa fa-thermometer-half' style='font-size: 22px !important;'></i> " . $patient->temperatura .
			" <i class='fa fa-clock-o' style='font-size: 22px !important;'></i> " . $patient->pressao .
			" <i class='fa fa-heartbeat' style='font-size: 20px !important;'></i> " . $patient->batimento . "</p>";
		$high .= "</div>";
	}
	foreach ($response->data->medium as $index => $patient) {
		if ($index == 0) {
			$medium = "";
		}
		$medium .= "<div class='mb-2'>";
		$medium .= "<p class='bg-warning m-0 text-white fw-bold'>" . $patient->nome . "</p><p class='bg-warning m-0 text-white fw-bold'>" .  $patient->idade . " anos | " . $patient->sexo . "</p>";
		$medium .= "<p class='bg-warning m-0 text-white'><label class='fw-bold'>SpO2: " . $patient->saturacao . "%</label>&nbsp;&nbsp;&nbsp;" .
			" <i class='fa fa-thermometer-half' style='font-size: 22px !important;'></i> " . $patient->temperatura .
			" <i class='fa fa-clock-o' style='font-size: 22px !important;'></i> " . $patient->pressao .
			" <i class='fa fa-heartbeat' style='font-size: 20px !important;'></i> " . $patient->batimento . "</p>";
		$medium .= "</div>";
	}
	foreach ($response->data->normal as $index => $patient) {
		if ($index == 0) {
			$normal = "";
		}
		$normal .= "<div class='mb-2'>";
		$normal .= "<p class='bg-primary m-0 text-white fw-bold'>" . $patient->nome . "</p><p class='bg-primary m-0 text-white fw-bold'>" .  $patient->idade . " anos | " . $patient->sexo . "</p>";
		$normal .= "<p class='bg-primary m-0 text-white'><label class='fw-bold'>SpO2: " . $patient->saturacao . "%</label>&nbsp;&nbsp;&nbsp;" .
			" <i class='fa fa-thermometer-half' style='font-size: 22px !important;'></i> " . $patient->temperatura .
			" <i class='fa fa-clock-o' style='font-size: 22px !important;'></i> " . $patient->pressao .
			" <i class='fa fa-heartbeat' style='font-size: 20px !important;'></i> " . $patient->batimento . "</p>";
		$normal .= "</div>";
	}
	echo json_encode(['success' => true, 'data' => ['high' => $high, 'medium' => $medium, 'normal' => $normal], 'alert' => $alert]);
	die();
}
echo json_encode($response);
