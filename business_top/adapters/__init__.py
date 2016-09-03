# -*- coding: utf-8 -*-

'''
所有交易和数据接口相关的适配器
'''

from program_top.components import component_base

class md_td_adapter_base(component_base):
	'''
	数据适配器基类，负责制作连续主力合约之类的交易标的，同时它的各个继承类负责将数据转换成需要的feed实例(depends on 不同的交易工具库)
	'''

	def __init__(self,binding_instance):
		super(md_td_adapter_base, self).__init__(binding_instance)
		pass
	pass

