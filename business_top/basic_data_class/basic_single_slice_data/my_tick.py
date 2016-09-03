# -*- coding: utf-8 -*-
from __future__ import division
from program_top.utilities import my_datetime

from program_top.utilities.pure_empty_class import pure_empty_class
from ..basic_single_slice_data import basic_single_slice_data

class my_tick(basic_single_slice_data):
	def __init__(self,tick_dict):
		gm_tick=pure_empty_class()
		gm_tick.__dict__.update(tick_dict)#使用更新字典的招数把字典还原成类实例

		self.cum_turnover=gm_tick.cum_amount
		self.cum_volume=gm_tick.cum_volume
		self.current_tick_turnover=gm_tick.last_amount
		self.current_tick_volume=gm_tick.last_volume
		self.tick_end_price=gm_tick.last_price

		if gm_tick.asks.__len__()<=0:
			self.s1_price=None
			self.s1_volume=None
		else:
			self.s1_volume=gm_tick.asks[0][1]
			self.s1_price=gm_tick.asks[0][0]
			pass

		if gm_tick.bids.__len__()<=0:
			self.b1_price=None
			self.b1_volume=None
		else:
			self.b1_volume=gm_tick.bids[0][1]
			self.b1_price=gm_tick.bids[0][0]
			pass

		self.current_tick_moment=my_datetime.utc_float2datetime(gm_tick.utc_time)
		pass
	pass

