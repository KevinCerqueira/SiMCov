from servertcp import ServerTCP
from serverudp import ServerUDP
from multiprocessing import Process

if __name__ == '__main__':
	tcp = ServerTCP()
	udp = ServerUDP()
	thread_tcp = Process(target=tcp.work, args=('tcp',))
	thread_udp = Process(target=udp.work, args=('tcp',))
	print('START TCP')
	thread_tcp.start()
	print('START UDP')
	thread_udp.start()