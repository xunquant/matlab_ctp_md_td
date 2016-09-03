# -*- coding: utf-8 -*-
from pyalgotrade.strategy import BacktestingStrategy,BaseStrategy
from datetime import datetime
from program_top.stdafx.trading_constants import trading_constants
from program_top.adapters.data_adapters import my_quant_data2pyalgo_csvfeed

class pyalgotrade_strategy_interface(BaseStrategy):
	'''
	pyalgotrade接口实例，继承pyalgo的策略，执行模拟盘和交易，不负责回验
	'''
	def __init__(self,my_strategy_ref=None):
		super(pyalgotrade_strategy_interface, self).__init__()
		pass

	def onBars(self, bars):

		pass
	pass

class pyalgotrade_backtest_interface(BacktestingStrategy):
	def onBars(self, bars):
		pass

	def __init__(self,my_strategy_ref=None):

		self._backtest_start_moment=datetime.combine(my_strategy_ref._backtest_start.date(),trading_constants['trading_day_start_moment'])
		self._backtest_end_moment=datetime.combine(my_strategy_ref._backtest_end.date(),trading_constants['trading_day_end_moment'])
		self._data_frequency=my_strategy_ref._data_period
		testing_feed=my_quant_data2pyalgo_csvfeed(my_strategy_ref._trading_target,self._data_frequency,self._backtest_start_moment,self._backtest_end_moment)#zcut




		super(pyalgotrade_backtest_interface, self).__init__()

		pass


	pass