<?php
define('MYPATH', '');
include_once('auth.php');
include_once('pages/templates/register_patient.php');
include_once('pages/templates/header.php');
?>
<style>
	#menu .btn {
		width: 15rem;
		height: 10rem;
	}

	.container {
		position: relative;
		top: 50%;
		transform: translateY(-50%);
	}

	a {
		text-decoration: none;
		color: #FFF !important;
	}

	i {
		color: #FFF;
		font-size: 50px !important;
	}
</style>
<title>Dashboard</title>
<div class="p-5 bg-light m-0" style="height: 100vh;">
	<div class="container m-0">
		<div class="row bg-white p-3 rounded shadow-sm mb-5">
			<p class="h2 text-center">
				SiMCov
				<i class="fa fa-user-md" style="color: #000;"></i>
			</p>
		</div>
		<div id="menu" class="text-center bg-white p-3 rounded shadow">
			<div class="row mb-3">
				<div class="col-md-4">
					<button class="btn btn-primary btn-block" data-bs-toggle="modal" data-bs-target="#register-patient">
						<p class="h2">Registrar novo paciente</p>
						<i class="fa fa-user"></i>
					</button>
				</div>
				<div class="col-md-4">
					<a id="list-priority" class="btn btn-danger" href="pages/list_priority.php">
						<p class="h2">Ver lista de prioridade</p>
						<i class="fa fa-th-list"></i>
					</a>
				</div>
				<div class="col-md-4">
					<button class="btn btn-warning">
						<p class="h2"><a href="measure.php">Medir um paciente</a></p>
						<i class="fa fa-heartbeat"></i>
					</button>
				</div>
			</div>
			<div class="row">
				<div class="col-md-6">
					<button class="btn btn-danger btn-block">
						<p class="h2">Apagar um paciente</p>
						<i class="fa fa-trash"></i>
					</button>
				</div>
				<div class="col-md-6">
					<button id="logout" class="btn btn-warning">
						<p class="h2 text-white">Sair do sistema
						</p>
						<i class="fa fa-sign-out mt-2"></i>
					</button>
				</div>
			</div>

		</div>
	</div>
</div>
<script>
	$('#logout').click(() => {
		return window.location = 'pages/auth/logout.php';
	});
</script>
<?php include_once('pages/templates/footer.php'); ?>