import socket
HOST = 'localhost'  # Endereco IP do Servidor
PORT = 50000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
msg = 'OIOIOIOI'

udp.sendto (bytes(msg.encode('utf-8')), dest)
print(udp.recvfrom(s))
udp.close()