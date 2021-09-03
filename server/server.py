import socket
import json

class Server:

	HOST = 'localhost'
	PORT = 50000
	
	server_socket = None

	def __init__(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((self.HOST, self.PORT))
		self.server_socket.listen(5)
		print('Server ON\n')
		self.work()
	
	def work(self):
		while True:
			print('PORT: ', self.PORT)
			connection, address = self.server_socket.accept()
			print('ADDRESS: ', address)
			
			method = ''
			path = ''
			data = None
			
			request = connection.recv(8192).decode('utf-8')
			for content in request.split('--'):
				if(content[: content.find(':')] == 'method'):
					method = content.replace('method:', '')
				elif(content[: content.find(':')] == 'path'):
					path = content.replace('path:', '')
				elif(content[: content.find(':')] == 'data'):
					data = json.loads(content.replace('data:', ''))
	
	def routing(self, method, path, data):
		if(method == 'POST'):
			if(path == 'register/patient'):
				pass
					
				
				
			
if __name__ == '__main__':
	server = Server()
	server.work()
			