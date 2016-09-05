# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class.working_type_base.front_end_base import front_end_base
from business_top.ctp_md_forwarder.ctp_gateway_new import CtpGateway

class ctp_md_forwarder(front_end_base):
	'''
	ctp行情转发服务器实例
	'''
	
	def __init__(self,enviroment_pack):
		super(ctp_md_forwarder, self).__init__(enviroment_pack)
		
		self._instruments_listening_client={}#监听合约行情的客户端列表，键是合约值是客户端的IP和端口，收到此合约的行情就向值中对应的IP和端口发送
		
		self._ctp_gateway=CtpGateway(self)
		
		pass
	
	
	
	
	
	
	
	
	pass