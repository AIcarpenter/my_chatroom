import myThread

def main():
	hosts={"127.0.0.1":"carpenter"}
	myThread.messageListenThread(hosts)


if __name__ == '__main__':
	main()