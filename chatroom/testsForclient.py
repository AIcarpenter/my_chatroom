#! coding:utf-8
import myThread
import message
def main():
	hosts={"172.29.153.167":"carpenter"}
	m=message.message('127.0.0.1',unicode('你好!','utf8'),hosts)
	myThread.messageShowThread(m.pack(),hosts)

if __name__ == '__main__':
	main()