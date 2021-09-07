import socket
import json
import sys
import os
import threading
import base64
import re
from collections import deque
from controldb import ControlDB
class Server:

	HOST = 'localhost'
	PORT = 50000
	
	# Servidor
	server_socket = None
	
	# Controlador da base de dados
	database = None
	
	queue_request = None
	thread_request = None
	
	close = False
	
	def __init__(self):
		# Iniciando o Server
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((self.HOST, self.PORT))
		self.server_socket.listen(5)
		self.controldb = ControlDB()
		self.queue_request = deque()
		self.thread_request = threading.Thread(target=self.queueRequest)
		self.thread_request.start()
		print('SERVER ON\n')
		self.work()
	
	# Função principal, onde o servidor irá receber as conexões
	def work(self):
		while not self.close:
			print('PORT: ', self.PORT)
			client, address = self.server_socket.accept()
			print('ADDRESS: ', address)
			
			self.receptor(client)
		
		if(self.close and len(self.queue_request) == 0):
			print('SERVER OFF')
			self.server_socket.close()
			return sys.exit()
	
	# Trata os dados recebidos
	def receptor(self, client):
		method = ''
		path = ''
		data = None
		token = ''
		
		request_raw = client.recv(8192)
		
		request_clean = str(request_raw.decode('utf-8'))
		
		content_parts = request_clean.split(' ')
		method = content_parts[0].replace(' ', '')
		path = content_parts[1].replace(' ', '')
		
		# Buscando o campo 'Authorization' na requisicao
		for itr in str(request_raw).split('\\r\\n'):
			if('Authorization:' in itr):
				itr = itr.replace(' ', '')
				token = re.sub('Basic|Bearer|Authorization:', '', itr)
				# auth_decode = base64.b64decode(auth).decode('utf-8')
		
		# Buscando por dados enviados na requisicao
		for index in request_clean:
			if(index == '{'):
				data = json.loads(request_clean[request_clean.find('{') :])
		
		# Adicionando a requisição a fila de requisições
		self.queue_request.append({'client': client,'method': method, 'path': path, 'data': data, 'token': token})
	
	# Consome a fila de requisições
	def queueRequest(self):
		while not (self.close and len(self.queue_request) == 0):
			if(len(self.queue_request) > 0):
				print('conn: ' + str(len(self.queue_request)))
				request = self.queue_request.popleft()
				self.routing(request['client'], request['method'], request['path'], request['data'], request['token'])
	
	# Função responsável pelo roteamente, identifica os metodos e as rotas requisitadas
	def routing(self, client, method, path, data, token):
		if(method == ''):
			self.sendToClientError('Requisicao invalida')
			
		# Requisições do tipo POST: para a criação de novos dados.
		elif(method == 'POST'):
			if(path == '/register/patient'):
				if(self.middleware(client, token)):
					self.registerPatient(client, token, data)
			elif(path == '/register/doctor'):
				self.registerDoctor(client, data)
			elif(path == '/login'):
				self.login(client, data)
			else:
				self.routeNotFound(client)
				
		# Requisições do tipo GET: retornar dados.
		elif(method == 'GET'):
			if(path == '/'):
				print('Bem vindo ao sistema!')
			elif(path == '/get/patients'):
				if(self.middleware(client, token)):
					self.getPatients(client, token, data)
			elif('/get/patient/' in path):
				if(self.middleware(client, token)):
					patient_id = path.replace('/get/patient/', '')
					self.getPatient(client, token, patient_id)
			elif(path == '/close-connection'):
				self.closeConnection(client)
			elif(path == '/close-socket'):
				self.closeSocket(client)
			else:
				self.routeNotFound(client)
				
		# Requisições do tipo PATCH: para atualizações parciais de dados.
		elif(method == 'PATCH'):
			if('/update/' in path):
				attribute = path.replace('/update/', '') # /saturacao/batimento/pressao/temperatura
				if(attribute in ['saturacao', 'batimento', 'pressao', 'temperatura']):
					if(self.middleware(client, token)):
						self.updateAttribute(client, token, data, attribute)
				else:
					self.routeNotFound(client)
			else:
				self.routeNotFound(client)
				
		# Requisições do tipo PUT: para atualizações completas.
		elif(method == 'PUT'):
			if(path == '/update/patient'):
				if(self.middleware(client, token)):
					self.updatePatient(client, token, data)
			else:
				self.routeNotFound(client)
				
		# Requisições do tipo DELETE: para deleções.
		elif(method == 'DELETE'):
			if(path == '/delete/patient'):
				if(self.middleware(client, token)):
					self.deletePatient(client, token, data)
			else:
				self.routeNotFound(client)
		else:
			self.routeNotFound(client)
		
		return client.close()
	
	# Fecha a conexão do cliente
	def closeConnection(self, client):
		client.close()
	
	# Desliga o servidor
	def closeSocket(self, client):
		print('SERVIDOR FECHARA AO TERMINAR AS CONEXOES EXISTENTES')
		self.close = True
	
	# Envia dados para o cliente
	# def sendToClient(self, client, obj):
	# 	return client.sendall(bytes(obj.encode('utf-8')))
	
	# Envia dados para o cliente em caso de sucesso
	def sendToClientOk(self, client, obj):
		response = json.dumps({'success': True, 'data': obj})
		return client.sendall(bytes(response.encode('utf-8')))
	
	# Envia dados para o cliente em caso de erro
	def sendToClientError(self, client, msg):
		response = json.dumps({'success': False, 'error': msg})
		return client.sendall(bytes(response.encode('utf-8')))
	
	# Autoriza ou não a autenticação do usuário
	def middleware(self, client, token):
		if(token == None):
			response = json.dumps({'success': False, 'error': 'Usuario nao autenticado.'})
			client.sendall(bytes(response.encode('utf-8')))
			return False
		if(not self.controldb.checkToken(token)):
			response = json.dumps({'success': False, 'error': 'Autenticacao invalida.'})
			client.sendall(bytes(response.encode('utf-8')))
			return False
		return True
	
	# Caso a rota informada não esteja dentre as disponiveis
	def routeNotFound(self, client):
		return self.sendToClientError(client, 'Rota nao encontrada')
	
	# Registra um novo medico.
	def registerDoctor(self, client, data):
		auth = "{}:{}".format(data['username'], data['password'])
		token = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
		success = self.controldb.createDoctor(data['username'], token)
		response = {'token': token}
		
		if(not success):
			return self.sendToClientError(client, 'Este nome ja esta em uso! Por favor, escolha outro.')
			
		return self.sendToClientOk(client, response)
	
	# Loga o medico retornando o token de acesso
	def login(self, client, data):
		auth = "{}:{}".format(data['username'], data['password'])
		token = self.controldb.getTokenByLogin(data['username'], base64.b64encode(auth.encode('utf-8')).decode('utf-8'))
		response = {'token': token}
		
		if(token == None):
			return self.sendToClientError(client, 'Credenciais invalidas!')
			
		return self.sendToClientOk(client, response)
	
	# Registra um novo paciente
	def registerPatient(self, client, token, data):
		doctor = self.controldb.getDoctorByToken(token)
		return self.sendToClientOk(client, {'id': self.controldb.createPatient(doctor['username'], data)})
	
	# Retorna todos os pacientes
	def getPatients(self, client, token, data):
		doctor = self.controldb.getDoctorByToken(token)
		return self.sendToClientOk(client, {'patients': self.controldb.getPatientsByDoctor(doctor['username'])})
	
	# Retorna um paciente em específico
	def getPatient(self, client, token, data):
		doctor = self.controldb.getDoctorByToken(token)
		return self.sendToClientOk(client, self.controldb.getPatientByDoctor(doctor['username'], data))
	
	# Atualiza determinado atributo de um paciente
	def updateAttribute(self, client, token, data, attr):
		doctor = self.controldb.getDoctorByToken(token)
		patient_id = data['id']
		value_attr = data['value'] 
		success = self.controldb.updateAttribute(doctor['username'], patient_id, attr, value_attr)
		if(success == False):
			return self.sendToClientError('Nao foi possivel atualizar medicao.')
		return self.sendToClientOk(client, success)
	
	# Atualiza todos os atributos de um paciente
	def updatePatient(self, client, token, data):
		doctor = self.controldb.getDoctorByToken(token)
		patient_id = data['id']
		success = self.controldb.updatePatient(doctor['username'], patient_id, data)
		if(success == False):
			return self.sendToClientError('Nao foi possivel atualizar medicoes.')
		return self.sendToClientOk(client, success)
	
	# Deleta um paciente
	def deletePatient(self, client, token, data):
		doctor = self.controldb.getDoctorByToken(token)
		patient_id = data['id']
		success = self.controldb.deletePatient(doctor['username'], patient_id)
		if(success == False):
			return self.sendToClientError('Nao foi possivel deletar o paciente.')
		return self.sendToClientOk(client, success)			
			
if __name__ == '__main__':
	server = Server()
	server.work()
			