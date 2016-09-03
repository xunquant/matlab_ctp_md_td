# -*- coding: utf-8 -*-


from business_top.adapters.my_quants import my_quant_adapter
from program_top.components.standalone_working_class.working_type_base.front_end_base import front_end_base

class my_strategy_base(front_end_base):
	'''
	我的策略基类，任何交易用具的接口都将作为一个interface来加载
	'''

	def __init__(self,current_environment_pack):
		super(my_strategy_base, self).__init__(current_environment_pack)

		pass

	def __initialisating_data_connections(self):
		'''
		连接数据平台
		'''
		self.adapters={'my_quant_adapter':my_quant_adapter(self)}


		pass


	pass