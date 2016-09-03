# -*- coding: utf-8 -*-

from datetime import timedelta
from ..trading_data_series import trading_data_series

class bar_data_session(trading_data_series):

	def __init__(self, data_content_name,data_period,session_start,session_end):
		super(bar_data_session, self).__init__(session_start=session_start, session_end=session_end,data_content_name=data_content_name,data_period=data_period)
		pass

	def _extract_bar_data(self, target_contract, session_start, session_end):
		'''
		提取目标数据的bar
		'''
		if self._data_period>=timedelta(days=1):#如果是日线
			self._extract_daily_bar(target_contract,session_start,session_end)
			return
		else:
			self._extract_min_bar(target_contract,session_start,session_end)
			return
			pass
		pass
	pass