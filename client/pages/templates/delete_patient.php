<?php
include_once('Controllers/patients.php');
?>
<div class="modal fade" id="delete-patient" tabindex="-1" aria-labelledby="delete-patientLabel" aria-hidden="true">
	<div class="modal-dialog modal-dialog-centered">
		<div class="modal-content">
			<form id="form-delete-patient">
				<div class="modal-header">
					<h5 class="modal-title" id="delete-patientLabel"><i class="fa fa-user" style="color: #000; font-size: 25px !important;"></i> Deletar um paciente</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
				</div>
				<div class="modal-body">
					<?php if ($search_patients->success) { ?>
						<div class="row">
							<div class="col-md-12"><label for="name-patient">Nome do paciente:</label>
								<select id="select-delete" required name="id">
									<option selected id="default" value=""></option>
									<?php foreach ($search_patients->data->patients as $patient) { ?>
										<option value="<?php echo $patient->id; ?>"><?php echo $patient->nome; ?></option>
									<?php } ?>
								</select>
							</div>
						</div>
					<?php } else { ?>
						<div hidden id="alert-error" class="alert alert-danger" role="alert">
							<p id="alert-text-error" class="h5 m-0"><? echo $search_patients->error; ?></p>
						</div>
					<?php } ?>
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
		$('#select-delete').select2({
			dropdownParent: $('#delete-patient'),
			placeholder: 'Selecione um paciente',
			dropdownAutoWidth: true,
			escapeMarkup: function(text) {
				return text;
			},
			width: "100%",
			language: "pt-BR",
			cache: true,
			// matcher: (params, data) => {if(params.nome == data) return data;},
			// ajax: {
			// 	url: '<?php echo MYPATH; ?>Controllers/patients.php',
			// 	dataType: 'json',
			// 	type: 'GET',
			// 	processResults: function(data) {
			// 		response = data
			// 		if (response.success) {
			// 			return {
			// 				results: $.map(response.data.patients, function(item) {
			// 					return {
			// 						text: item.nome,
			// 						id: item.id,
			// 					};
			// 				}),
			// 			};
			// 		}

			// 	},
			// }
		});


		$('#form-delete-patient').submit(function(event) {
			event.preventDefault();
			let id = $('#delete-patient').find(':selected').val();
			$.ajax({
				type: "POST",
				url: "<?php echo MYPATH; ?>Controllers/delete_patient.php",
				data: $('#form-delete-patient').serialize(),
				success: function(data) {
					response = JSON.parse(data);
					if (response.success) {
						Swal.fire(
							'Paciente deletado com sucesso! ',
							'',
							'success'
						);
						$('.inputs').val('');
						$('#delete-patient').modal('toggle');
						$("#delete-patient option[value="+id+"]").remove();
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