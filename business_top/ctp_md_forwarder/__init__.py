# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class.working_type_base.front_end_base import front_end_base
from extensions.ctpGateway.ctpGateway import CtpMdApi

class ctp_md_forwarder(front_end_base):
	'''
	ctp行情转发服务器实例
	'''
	
	def __init__(self):
		self.__md_instance=CtpMdApi()
		
		pass
	
	
	
	
	
	
	
	
	pass