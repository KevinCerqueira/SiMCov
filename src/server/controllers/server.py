import socket

HOST = 'localhost'
PORT = 50000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print('Aguardando')
conn, address = server.accept()

print('Conectado em', address)
while True:
	data = conn.recv(1024)
	if not data:
		print('Fechando')
		conn.close()
		break
	conn.sendall(data)