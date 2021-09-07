import socket
import json
import sys
import os
import threading
import base64
import re
from controldb import ControlDB
class Server:

	HOST = 'localhost'
	PORT = 50000
	
	server_socket = None
	
	database = None
	
	count_connections = 0
	
	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((self.HOST, self.PORT))
		self.server_socket.listen(5)
		self.database = ControlDB()
		print('SERVER ON\n')
		self.work()
	
	def work(self):
		while True:
			print('PORT: ', self.PORT)
			client, address = self.server_socket.accept()
			print('ADDRESS: ', address)
			
			self.receptor(client)
		self.server_socket.close()
	
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
		
		for itr in str(request_raw).split('\\r\\n'):
			if('Authorization:' in itr):
				itr = itr.replace(' ', '')
				token = re.sub('Basic|Bearer|Authorization:', '', itr)
				# auth_decode = base64.b64decode(auth).decode('utf-8')
		
		for index in request_clean:
			if(index == '{'):
				data = json.loads(request_clean[request_clean.find('{') :])
				
		print(method, path, data, token)
		self.routing(client, method, path, data, token)
	
	def routing(self, client, method, path, data, token):
		# Requisições do tipo POST: para a criação de novos dados.
		if(method == 'POST'):
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
			elif('/get/' in path):
				path = path.replace('/get/', '')
				if(path == 'all'):
					return self.getAll(client)
				else:
					return self.getById(client, path)
			elif(path == '/close-connection'):
				return self.closeConnection()
			else:
				self.routeNotFound(client)
		# Requisições do tipo PATCH: para atualizações parciais de dados.
		elif(method == 'PATCH'):
			if('/update/' in path):
				path = path.replace('/update/', '') # /saturacao/batimento/pressao/temperatura
				return self.updateAttr(client, data, path)
			else:
				self.routeNotFound(client)
				
		# Requisições do tipo PUT: para atualizações completas.
		elif(method == 'PUT'):
			if(path == '/update'):
				return self.update(client, data)
			else:
				self.routeNotFound(client)
		# Requisições do tipo DELETE: para deleções
		elif(method == 'DELETE'):
			if(path == '/delete'):
				return self.delete(client, data)
			else:
				self.routeNotFound(client)
			
		self.server_socket.close()
		sys.exit()
	
	def closeConnection(self, client):
		client.close()

	def sendToClient(self, client, obj):
		return client.sendall(bytes(obj.encode('utf-8')))
	
	def sendToClientOk(self, client, obj):
		response = json.dumps({'success': True, 'data': obj})
		return client.sendall(bytes(response.encode('utf-8')))
	
	def sendToClientError(self, client, msg):
		response = json.dumps({'success': False, 'error': msg})
		return client.sendall(bytes(response.encode('utf-8')))
	
	def middleware(self, client, token):
		if(not self.database.checkToken(token)):
			response = json.dumps({'success': False, 'error': 'Usuario nao autenticado.'})
			client.sendall(bytes(response.encode('utf-8')))
			return False
		return True
	
	def routeNotFound(self, client):
		return self.sendToClientError(client, 'Rota nao encontrada')
	
	def getAll(self, client):
		return self.sendToClientOk(client, self.database.getAll())
		
	def getById(self, client, id):
		return self.sendToClientOk(client, self.database.get(id))
	
	def registerDoctor(self, client, data):
		auth = "{}:{}".format(data['username'], data['password'])
		token = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
		success = self.database.createDoctor(data['username'], token)
		response = {'token': token}
		
		if(not success):
			return self.sendToClientError(client, 'Este nome ja esta em uso! Por favor, escolha outro.')
			
		return self.sendToClientOk(client, response)
	
	def login(self, client, data):
		auth = "{}:{}".format(data['username'], data['password'])
		token = self.database.getTokenByLogin(data['username'], base64.b64encode(auth.encode('utf-8')).decode('utf-8'))
		response = {'token': token}
		
		if(token == None):
			return self.sendToClientError(client, 'Credenciais invalidas!')
			
		return self.sendToClientOk(client, response)
	
	def registerPatient(self, client, token, data):
		doctor = self.database.getDoctorByToken(token)
		self.sendToClientOk(client, {'id': self.database.createPatient(doctor['username'], data)})
	
	def updateAttr(self, client, data, attr):
		success = json.dumps({'success': self.database.updateAttribute(data['id'], attr, data['value'])})
		self.sendToClient(client, success)
	
	def update(self, client, data):
		success = json.dumps({'success': self.database.update(data['id'], data)})
		self.sendToClient(client, success)
	
	def delete(self, client, data):
		success = json.dumps({'success': self.database.delete(data['id'])})
		self.sendToClient(client, success)
	
				
			
if __name__ == '__main__':
	server = Server()
	server.work()
			