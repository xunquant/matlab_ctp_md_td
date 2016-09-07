# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class.working_type_base.front_end_base import front_end_base
from business_top.ctp_md_forwarder.ctp_gateway_new import CtpGateway
from program_top.utilities.my_timer import my_zmq_timer
from datetime import timedelta,datetime

class ctp_md_forwarder(front_end_base):
	'''
	ctp行情转发服务器实例
	'''
	
	def __init__(self,enviroment_pack):
		super(ctp_md_forwarder, self).__init__(enviroment_pack)
		
		self._instruments_listening_client={}#监听合约行情的客户端列表，键是合约值是客户端的IP和端口，收到此合约的行情就向值中对应的IP和端口发送
		
		self._ctp_gateway=CtpGateway(self)
		self._register_event_and_processor()
		
		
		
		pass
	
	def __subscription_in(self,subscription_json):
		'''
		行情订阅的json入口
		'''
		
		pass
	pass