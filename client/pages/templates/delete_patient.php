<div class="modal fade" id="delete-patient" tabindex="-1" aria-labelledby="delete-patientLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<form name="form-delete">
				<div class="modal-header">
					<h5 class="modal-title" id="delete-patientLabel"><i class="fa fa-user" style="color: #000; font-size: 25px !important;"></i> Deletar um paciente</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-12"><label for="name-patient">Nome do paciente:</label>
							<select class="select-delete" name="id">
							</select>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
					<button type="submit" class="btn btn-danger">Deletar</button>
				</div>
			</form>
		</div>
	</div>
</div>
<script>
	$(function() {
		// $('#btn-apagar-paciente').click(() => {
		$('.select-delete').select2({
			placeholder: 'Selecione um paciente',
			dropdownAutoWidth: true,
			escapeMarkup: function(text) {
				return text;
			},
			width: "100%",
			language: "pt-BR",
			cache: true,
			ajax: {
				url: '<?php echo MYPATH; ?>Controllers/patients.php',
				dataType: 'json',
				type: 'GET',
				processResults: function(data) {
					response = JSON.parse(data);
					console(response.success);
					if (response.success) {
						return {
							results: $.map(response.data.patients, function(item) {
								return {
									text: item.nome,
									id: item.id,
								};
							}),
						};
					}

				},
			}
		});
		// })

		$('#form-delete').submit(function(event) {
			event.preventDefault();
			$.ajax({
				type: "POST",
				url: "<?php echo MYPATH; ?>Controllers/delete_patient.php",
				data: $('#form-delete').serialize(),
				success: function(data) {
					response = JSON.parse(data);
					if (response.success) {
						Swal.fire(
							'Paciente deletado com sucesso! ',
							'',
							'success'
						);
						$('.inputs').val('');
					} else {
						Swal.fire(
							'Houve um erro ao deletar o paciente.',
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
	});
</script>