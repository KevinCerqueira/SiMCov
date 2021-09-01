import socket

HOST = '127.0.0.1'
PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(str.encode('Kevin'))

data = client.recv(1024)
print('Msg', data.decode())