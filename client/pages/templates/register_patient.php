<div class="modal fade" id="register-patient" tabindex="-1" aria-labelledby="register-patientLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<div class="modal-header">
				<h5 class="modal-title" id="register-patientLabel"><i class="fa fa-user" style="color: #000; font-size: 25px !important;"></i> Registrar novo paciente</h5>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
			</div>
			<form id="form-register-patient">
				<div class="modal-body">
					<div class="">
						<div class="mb-3">
							<label for="name-patient">Nome do paciente:</label>
							<input required type="text" class="form-control inputs" name="nome" title="É necessário um nome para o paciente.">
						</div>
						<div class="mb-3 row">
							<div class="col-md-6">
								<label for="age-patient">Idade:</label>
								<input required type="number" class="form-control inputs" name="idade" title="É necessário informar a idade do paciente.">
							</div>
							<div class="col-md-6">
								<label for="gender-patient">Sexo:</label>
								<select required name="sexo" id="gender-patient" class="form-control">
									<option value="F">Feminino</option>
									<option value="M">Masculino</option>
								</select>
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
					<button type="submit" class="btn btn-primary">Cadastrar</button>
				</div>
			</form>
		</div>
	</div>
</div>
<script src="vendor/jquery/jquery.js"></script>
<script>
	$('#form-register-patient').submit(function(event) {
		event.preventDefault();
		$.ajax({
			type: "POST",
			url: "<?php echo MYPATH;?>Controllers/register_patient.php",
			data: $('#form-register-patient').serialize(),
			success: function(data) {
				response = JSON.parse(data);
				if (response.success) {
					Swal.fire(
						'Paciente cadastrado com sucesso! ',
						'ID: ' + response.data.id,
						'success'
					);
					$('.inputs').val('');
				} else {
					Swal.fire(
						'Houve um erro ao cadastrar o paciente.',
						'Erro: ' + response.error,
						'error'
					);
				}
			},
			error: function(data) {
				Swal.fire(
					'Parece que estamos offline, chame o TI.',
					'',
					'error'
				);
			}
		});
	});
</script>