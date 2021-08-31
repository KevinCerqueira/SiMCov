import socket

HOST = '127.0.0.1'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print('Aguardando')

conn, ender = s.accept()

print('Conectado em', ender)
while True:
	data = conn.recv(1024)
	if not data:
		print('Fechando')
		conn.close()
		break
	conn.sendall(data)