import os
import sys
import json

# Classe para controlar a base de dados.
class ControlDB:
	db_path = '\\database\\'
	db_name = 'database'
	db_extension = '.json'
	
	db_user_path = '\\database\\doctors.json'
	db_patient_path = '\\database\\patients\\'
	
	directory = ''
	
	def __init__(self):
		self.directory = os.path.dirname(os.path.realpath(__file__))
	
	def createDoctor(self, username, auth):
		# Checando se já existe um usuario com o username igual
		if(self.checkUsername(username)):
			return False
		# Novos dados para adicionar a base
		id_doctor = int(self.getLastId(self.db_user_path)) + 1
		new_doctor = {'id': id_doctor, 'username': username, 'auth': auth}
		# Criando pasta e arquivo de pacientes do médico
		try:
			os.mkdir(self.directory + self.db_patient_path + username)
		except:
			pass
		finally:
			with open(self.directory + self.db_patient_path + username + '\\patients.json', 'w', encoding='utf-8') as file:
				json.dump({}, file, ensure_ascii=False, indent=2)
		# Atualizando o arquivo dos medicos
		current_data = self.getAll(self.db_user_path)
		current_data[str(id_doctor)] = new_doctor
		with open(self.directory + self.db_user_path, 'w', encoding='utf-8') as db_write:
			json.dump(current_data, db_write, ensure_ascii=False, indent=4)
		return True
	
	# Cadastrar novo paciente
	def createPatient(self, doctor_username, data):
		self.checkDoctorPath(doctor_username)
		new_id = int(self.getLastId(self.db_patient_path + doctor_username + '\\patients.json')) + 1
		new_data = {'id': new_id, 'nome': data['nome'], 'medicao': False, 'saturacao': 0, 'pressao': 0, 'batimentos': 0, 'temperatura': 0}
		current_data = self.getAll(self.db_patient_path + doctor_username + '\\patients.json')
		current_data[str(new_id)] = new_data
		with open(self.directory + self.db_patient_path + doctor_username + '\\patients.json', 'w', encoding='utf-8') as db_write:
			json.dump(current_data, db_write, ensure_ascii=False, indent=4)
		return new_id
	
	# Retornar último ID cadastrado.
	def getLastId(self, db_file):
		last_id = -1 # Retorna -1 caso não tenha nada.
		with open(self.directory + db_file, 'r', encoding='utf-8') as db_read:
			data = json.load(db_read)
			for id in data:
				last_id = id
		return last_id
	
	# Retornar todos os dados.
	def getAll(self, db_file):
		with open(self.directory + db_file, 'r', encoding='utf-8') as db_read:
			return json.load(db_read)
		return None
	
	def checkUsername(self, username):
		with open(self.directory + self.db_user_path, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(data_read[id_read]['username'] == username):
					return True
		return False
	
	def checkDoctorPath(self, username):
		try:
			os.mkdir(self.directory + self.db_patient_path + username)
		except:
			pass
	
	def getTokenByLogin(self, username, auth):
		with open(self.directory + self.db_user_path, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(data_read[id_read]['username'] == username and data_read[id_read]['auth'] == auth):
					return data_read[id_read]['auth']
		return None
	
	def getDoctorByToken(self, token):
		with open(self.directory + self.db_user_path, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(data_read[id_read]['auth'] == token):
					return data_read[id_read]
		return None
	
	def checkToken(self, token):
		with open(self.directory + self.db_user_path, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(data_read[id_read]['auth'] == token):
					return True
		return False
	
	# Retornar último ID cadastrado.
	# def getLastId(self):
	# 	last_id = -1
	# 	with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
	# 		data = json.load(db_read)
	# 		for id in data:
	# 			last_id = id
	# 	return last_id
	
	# Retornar todos os dados.
	# def getAll(self):
	# 	data = None
	# 	with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
	# 		data = json.load(db_read)
	# 	return json.dumps(data)
	
	# Retornar um paciente em especifico.
	def getDoctorById(self, id):
		with open(self.directory + self.db_user_path, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					return json.dumps(data_read[id_read])
		return None
	
	def getDoctorByUsername(self, username):
		with open(self.directory + self.db_user_path, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(data_read[id_read]['username'] == username):
					return data_read[id_read]
		return False
	
	# Retornar um paciente em especifico.
	def get(self, id):
		with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					return json.dumps(data_read[id_read])
		return None
	
	# Retornar um paciente em especifico.
	def get(self, id):
		with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					return json.dumps(data_read[id_read])
		return None
	
	# Verifica se existe determinado ID.
	def has(self, id):
		with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					return True
		return False
	
	# Atualiza os dados de um paciente por completo.
	def update(self, id, data):
		if(not self.has(id)):
			return False
			
		with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					data_read[id_read] = {'nome': data['nome'], 'medicao': True, 'saturacao': data['saturacao'], 'pressao': data['pressao'], 'batimento': data['batimento']}
					with open(self.directory + self.db_path + self.db_name + self.db_extension, 'w', encoding='utf-8') as db_write:
						json.dump(data_read, db_write, ensure_ascii=False, indent=4)
					return True
		return False	
	
	# Atualiza um atributo em especifico de determinado paciente.
	def updateAttribute(self, id, attr, value):
		if(not self.has(id)):
			return False
			
		with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					data_read[id_read][attr] = value
					with open(self.directory + self.db_path + self.db_name + self.db_extension, 'w', encoding='utf-8') as db_write:
						json.dump(data_read, db_write, ensure_ascii=False, indent=4)
					return True
		return False
	
	# Deleta um paciente por ID.
	def delete(self, id):
		if(not self.has(id)):
			return False
			
		with open(self.directory + self.db_path + self.db_name + self.db_extension, 'r', encoding='utf-8') as db_read:
			data_read = json.load(db_read)
			for id_read in data_read:
				if(str(id_read) == str(id)):
					data_read.pop(id)
					with open(self.directory + self.db_path + self.db_name + self.db_extension, 'w', encoding='utf-8') as db_write:
						json.dump(data_read, db_write, ensure_ascii=False, indent=4)
					return True
		return False
		
if __name__ == "__main__":
	con = ControlDB()