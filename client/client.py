import socket
import json
import sys

HOST = 'localhost'
PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
# send = input()
# send = {'nome': 'Kevin', 'outro': 'kev'}
send = {'id': '2', 'value': 9999}
# client.sendall(str.encode('Kevin'))

# client.sendall('--method:POST --path:/register/patient --data:{}'.format(json.dumps(send)).encode('utf-8'))
client.sendall('PATCH /update/saturacao {}'.format(json.dumps(send)).encode('utf-8'))
	
data = client.recv(8192)
print('Msg', data.decode())
client.close()
sys.exit()