#! coding:utf-8
import threading
import socket
import message
import copy
from time import time

serverPort=12345
communicatePort=12346


class serverHeartbeatThread(threading.Thread):
	'''服务端心跳线程'''
	def __init__(self,remoteSocket,ipaddr,hostsList):
		threading.Thread.__init__(self);
		self.s=remoteSocket
		self.ipaddr=ipaddr
		self.hosts=hostsList
		self.start()

	def run(self):
		'''心跳检测'''
		seconds=time()-3
		nickname=self.s.recv(1024)
		self.hosts[self.ipaddr[0]]=nickname
		while True:
			flag=time()
			if flag-seconds>3:
				#print self.hosts
				seconds=flag
				try:
					#print "sending hosts.txt"
					self.s.send(str(self.hosts))
					res=self.s.recv(1024)
					#print "--%s--" % res
					if res!="ok":
						break;
				except :
					'''心跳消失'''
					break
		self.s.close()
		#print "-----------------",self.hosts.pop(self.ipaddr[0])

		
class clientHeartbeatThread(threading.Thread):
	'''客户端心跳线程'''
	def __init__(self,name,hosts=None):
		threading.Thread.__init__(self)
		self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.hosts=hosts
		self.nickname=name
		self.start()

	def run(self):
		try:
			self.s.connect(('101.200.205.154',serverPort))
			self.s.send(self.nickname)
		except :
			raise
		while True:
			try:
				rec=self.s.recv(1024)
				self.hosts.update(eval(rec))
				self.s.send("ok")
			except :
				break
		self.s.close()


class messageSendThread(threading.Thread):
	def __init__(self,hosts,message):
		threading.Thread.__init__(self)
		self.m=message
		self.hosts=hosts
		self.start()

	def run(self):
		if self.m.m['addr']['to']=='all':
			m=copy.deepcopy(m)
			for item in self.hosts:
				m.m['addr']['to']=item
				messageSubsendThread(m)
		else:
			messageSubsendThread(self.m)

		

class messageSubsendThread(threading.Thread):
	def __init__(self,message):
		threading.Thread(self)
		self.m=message
		self.start()

	def run(self):
		dirction=self.m.m['addr']
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.settimeout(2)
		count=3
		print dirction
		while count:
			try:
				s.sendto(self.m.pack(),(dirction['to'],communicatePort))
				#print "send done."
				data,_=s.recvfrom(1024)
				print data,type(data)
				if data=="ok":
					break
			except:
				raise
				count-=1
				pass


class messageListenThread(threading.Thread):
	def __init__(self,hosts):
		threading.Thread.__init__(self)
		self.hosts=hosts
		self.start()

	def run(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.bind(('',communicatePort))
		while True:
			try:
				data,addr=s.recvfrom(1024)
				s.sendto("ok",addr)
				messageShowThread(data,self.hosts)
			except:
				raise
				pass
				

class messageShowThread(threading.Thread):
	def __init__(self,datastr,hosts):
		threading.Thread.__init__(self)
		self.m=eval(datastr)
		self.hosts=hosts
		self.start()

	def _getNickname(self,ipaddr):
		return self.hosts[ipaddr]

	def run(self):
		nickname=self._getNickname(self.m['addr']['from'])
		print ">%s>>%s>>>%s\n\n" % (self.m['time'],nickname,self.m['words'])
