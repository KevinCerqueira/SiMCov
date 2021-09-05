import socket
import json
import sys
import os
from controldb import ControlDB
class Server:

	HOST = 'localhost'
	PORT = 50000
	
	server_socket = None
	
	database = None
	
	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((self.HOST, self.PORT))
		self.server_socket.listen(5)
		self.database = ControlDB()
		print('Server ON\n')
		self.work()
	
	def work(self):
		while True:
			print('PORT: ', self.PORT)
			client, address = self.server_socket.accept()
			print('ADDRESS: ', address)
			
			method = ''
			path = ''
			data = None
			
			request = str(client.recv(8192).decode('utf-8'))
			content_parts = request.split(' ')
			method = content_parts[0].replace(' ', '')
			path = content_parts[1].replace(' ', '')
			
			for index in request:
				if(index == '{'):
					data = json.loads(request[request.find('{') :])
			# print(method, path)
			# print(data)
			# for content in request.split(' '):
			# 	print(content)
			# 	if(content[: content.find(':')] == 'method'):
			# 		method = content.replace('method:', '')
			# 	elif(content[: content.find(':')] == 'path'):
			# 		path = content.replace('path:', '')
			# 	elif(content[: content.find(':')] == 'data'):
			# 		data = json.loads(content.replace('data:', ''))
			self.routing(client, method, path, data)
			sys.exit()
	
	def routing(self, client, method, path, data):
		# Requisições do tipo POST: para a criação de novos dados.
		if(method == 'POST'):
			if(path == '/register'):
				self.register(client, data)
		# Requisições do tipo GET: retornar dados.
		elif(method == 'GET'):
			print(path)
			if('/get/' in path):
				path = path.replace('/get/', '')
				if(path == 'all'):
					return self.getAll(client)
				else:
					return self.getById(client, path)
		# Requisições do tipo PATCH: para atualizações parciais de dados.
		elif(method == 'PATCH'):
			if('/update/' in path):
				path = path.replace('/update/', '') # /saturacao/batimento/pressao
				self.updateAttr(client, data, path)
				
		# Requisições do tipo PUT: para atualizações completas.
		elif(method == 'PUT'):
			if(path == '/update'):
				pass
		# Requisições do tipo DELETE: para deleções
		elif(method == 'DELETE'):
			if(path == '/delete'):
				pass
			
		self.server_socket.close()
		sys.exit()
		
	def sendToClient(self, client, obj):
		return client.sendall(bytes(obj.encode('utf-8')))
		
	def getAll(self, client):
		self.sendToClient(client, self.database.getAll())
		
	def getById(self, client, id):
		self.sendToClient(client, self.database.get(id))
		
	def register(self, client, data):
		self.sendToClient(client, self.database.insert(data))
	
	def updateAttr(self, client, data, attr):
		# print(data['id'])
		# print(data[0])
		self.sendToClient(client, self.database.updateAttribute(data['id'], attr, data['value']))
	
				
			
if __name__ == '__main__':
	server = Server()
	server.work()
			