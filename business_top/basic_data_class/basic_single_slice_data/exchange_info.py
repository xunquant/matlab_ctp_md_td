# -*- coding: utf-8 -*-

from ..basic_single_slice_data import basic_single_slice_data

class exchange_info_base(basic_single_slice_data):
	def __init__(self):
		self.exchange_code=self.__class__.__name__

	pass

class SHFE(exchange_info_base):
	def __init__(self):
		pass
	pass

class DCE(exchange_info_base):
	pass

class CZCE(exchange_info_base):
	pass

class CFFEX(exchange_info_base):
	pass

commodity_exchanges={
	'SHFE':SHFE,
	'DCE':DCE,
	'CZCE':CZCE
}