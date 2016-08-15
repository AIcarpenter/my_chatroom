#! coding:utf-8
from time import localtime,strftime
from socket import gethostbyname,gethostname,getfqdn
import socket

class message:
	def __init__(self,destination,words,hosts):
		self.destination=destination
		self.words=words
		self.hosts=hosts
		self.ISOTIMEFORMAT='%Y-%m-%d %X'
		self.m={}
		self.pack()

	def pack(self):
		self.m['words']=self.words
		self.m['time']=strftime(self.ISOTIMEFORMAT,localtime())
		self.m['addr']={}
		self.m['addr']['to']=self.destination
		self.m['addr']['from']=gethostbyname(getfqdn(gethostname()))
		return str(self.m)			
