import socket

HOST = '127.0.0.1'
PORT = 50000

s = socket.socket(socket.AF_INET, socket.SOCKET_STREAM)
s.connect((HOST, PORT))
s.sendall(str.encode('Kevin'))

data = s.recv(1024)
print('Msg', data.decode())