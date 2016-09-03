# -*- coding: utf-8 -*-
from __future__ import division
from program_top.utilities import my_datetime
from datetime import datetime

from ..basic_single_slice_data import basic_single_slice_data

class my_bar(basic_single_slice_data):
	def __init__(self, bar_dict):
		self.__dict__.update(bar_dict)#使用更新字典的招数把字典还原成类实例
		self.bar_start_time=datetime.strptime(self.strtime, my_datetime.my_quant_time_stamp_format)
		self.bar_end_time=my_datetime.utc_float2datetime(self.utc_time)
		self.__delattr__('strtime')
		self.__delattr__('utc_time')
		pass
	pass