#!coding:utf-8
import myThread
import socket
import message
def messageInput(hosts):
	inputwords=raw_input(">")
	item=inputwords.split(':')
	destination=item[0]
	words=item[1]
	m=message.message(destination,words,hosts)
	myThread.messageSendThread(hosts,m)

def main():
	nickname=raw_input("input your nickname please:")
	hosts={}
	thread=myThread.clientHeartbeatThread(nickname,hosts)
	thread=myThread.messageListenThread(hosts)
	while True:
		messageInput(hosts)

if __name__ == '__main__':
	main()
	