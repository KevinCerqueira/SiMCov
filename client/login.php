<?php
session_start();
if (isset($_SESSION['auth'])) {
	header('Location: index.php');
	exit;
}
if (isset($_POST['username']) && isset($_POST['password'])) {
	include_once('ClientController.php');
	$username = $_POST['username'];
	$password = $_POST['password'];
	$client = new ClientController();
	$response = $client->login($username, $password);
	if ($response === true) {
		header('Location: index.php');
		exit;
	} else {
		$_SESSION['error'] = $response;
	}
}
?>

<!DOCTYPE html>
<html lang="pt-br">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
	<title>Login</title>
</head>

<body>
	<div class="container p-5">
		<div class="card">
			<div class="card-body">
				<form action="login.php" method="post">
					<p class="h2 text-center">SiMCov</p>
					<?php if (isset($_SESSION['error'])) : ?>
						<div class="alert alert-danger" role="alert">
							<?php echo $_SESSION['error'];
							unset($_SESSION['error']); ?>
						</div>
					<?php endif; ?>
					<div class="mb-3">
						<label for="username" class="form-label">Seu nome de usuário:</label>
						<input type="text" name="username" id="username" class="form-control">
					</div>
					<div class="mb-3">
						<label for="username" class="form-label">Senha:</label>
						<input type="password" name="password" id="password" class="form-control">
					</div>
					<div class="mb-3">
						<button type="submit" class="btn btn-primary">Entrar</button>
					</div>
					<p>Não tem uma conta? <a href="register.php">Crie uma aqui.</a></p>
				</form>
			</div>
		</div>
	</div>

	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-/bQdsTh/da6pkI1MST/rWKFNjaCP5gBSY4sEBT38Q/9RBh9AH40zEOg7Hlq2THRZ" crossorigin="anonymous"></script>
</body>

</html>