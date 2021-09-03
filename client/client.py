import socket
import json

HOST = '127.0.0.1'
PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
send = input()
send = {'id': 'oi', 'nom': 'kev'}
# client.sendall(str.encode('Kevin'))

client.sendall('--method:GET --path:/register/patient --data:{}'.format(json.dumps(send)).encode())
	
client.close()
data = client.recv(1024)
print('Msg', data.decode())