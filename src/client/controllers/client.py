import socket

HOST = '127.0.0.1'
PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
send = input()
send = {'id': 'oi', 'nom': 'kev'}
# client.sendall(str.encode('Kevin'))

client.sendall('GET /{} HTTP/1.1\r\nHost:{}\r\n\r\n'.format(send, HOST).encode())
	

data = client.recv(1024)
print('Msg', data.decode())