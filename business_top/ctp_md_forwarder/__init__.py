# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class.working_type_base.front_end_base import front_end_base
from business_top.ctp_md_forwarder.ctp_gateway_new import CtpGateway
from program_top.utilities.my_timer import my_zmq_timer
from datetime import timedelta,datetime
import zmq,socket,os

class ctp_md_forwarder(front_end_base):
	'''
	ctp行情转发服务器实例
	'''
	
	def __init__(self,enviroment_pack):
		super(ctp_md_forwarder, self).__init__(enviroment_pack)
		
		self._instruments_listening_client={}#监听合约行情的客户端列表，键是合约值是客户端的IP和端口，收到此合约的行情就向值中对应的IP和端口发送
		
		self._ctp_gateway=CtpGateway(self)
		#self._register_event_and_processor()
		
		self.__socket_init()
		self.__period_worker=my_zmq_timer(first_emit_moment=datetime.now()+timedelta(seconds=1), emit_interval=timedelta(seconds=3), emit_function=self.sending_via_socket)
		pass
	
	def __socket_init(self):
		self.sink=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.target_address=("192.168.199.186",31416)
		self.sink.connect(self.target_address)
		self.__messege_count=0
		pass
	
	def sending_via_socket(self):
		print 'trying to send'
		
		try:
			
			current_messege=datetime.now().__repr__()+'message no:'+str(self.__messege_count)+os.linesep
			print current_messege
			self.sink.send(current_messege)#一定要注意，这里绝对不能传输中文，matlab那边接收中文就会无法按行接收字符串
			
		except Exception, current_exception:
			print current_exception
			pass
		
		self.__messege_count+=1
		#print current_messege
		
		pass
	
	
	def __subscription_in(self,subscription_json):
		'''
		行情订阅的json入口
		'''
		
		pass
	pass