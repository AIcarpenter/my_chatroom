#!coding:utf-8
import myThread
import socket

serverPort=12345

def main():
	listenSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		listenSocket.bind(('',serverPort))
		listenSocket.listen(5)
	except :
		raise
	while True:
		hosts={}
		client,ipaddr=listenSocket.accept()
		thread=myThread.serverHeartbeatThread(client,ipaddr,hosts)


if __name__ == '__main__':
	main()

