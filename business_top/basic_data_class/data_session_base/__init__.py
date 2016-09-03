# -*- coding: utf-8 -*-

import os
from datetime import timedelta

from business_top.basic_data_class import basic_data_class
from program_top.utilities.my_datetime import data_buffer_date_format,data_buffer_time_format


class data_session_base(basic_data_class):
	'''
	序列数据基类，包含交易数据的tick或者bar时间序列，账户净值序列和资产序列，盈亏序列
	'''

	def _get_serialised_filename(self):
		'''
		取得序列化后的文件名:标的代码，开始时间，结束时间，数据周期(频率)
		'''
		target_format= data_buffer_date_format if self._data_period>=timedelta(days=1) else data_buffer_time_format
		frequency=self._data_period.total_seconds()
		start_date_string=self._start_moment.strftime(target_format)
		end_date_string=self._end_moment.strftime(target_format)
		relative_filename=','.join([self._content_name,'series', str(frequency),self.__class__.__name__, start_date_string,end_date_string,'.json'])
		return relative_filename

	def __init__(self,data_content_name,data_period,session_start, session_end):
		super(data_session_base, self).__init__()
		session_start_type=session_start.__class__.__name__
		session_end_type=session_end.__class__.__name__

		if session_end_type!=session_start_type:
			print("开始时间和结束时间频率不相等")
			return

		self._series_data_type=self.__class__.__name__#序列数据类别就是最终子类的类名称
		self._data_period=data_period#应该是一个time_delta，表示序列中每个切片的时长，分钟k线就是min的time_delta，小时就是hourt的time_delta
		self._start_moment=session_start#序列开始时刻
		self._end_moment=session_end#序列结束时刻
		self._content_name=data_content_name#数据内容名称，如果是交易数据类别，那就是标的代码，含交易所代码，如果是账户净值或者账户金额，则为内容名称
		self._buffer_absolute_filename=my_path.buffer_file_dir+self._get_serialised_filename()

		self._load_if_data_buffered()
		pass

	def _load_if_data_buffered(self):
		'''
		若有数据，就加载数据文件
		'''
		if not os.path.isfile(self._buffer_absolute_filename):#如果缓存文件不存在
			if self._data_period.total_seconds()<1:#如果是tick数据
				print '这是tick数据'#till here，到时加载tick数据
				return
			else:
				self._extract_bar_data(target_contract=self._content_name,session_start=self._start_moment,session_end=self._end_moment)
				return
		else:
			self._load_from_file(self._buffer_absolute_filename)
		pass

	def _extract_bar_data(self, target_contract, session_start, session_end):
		'''
		提取目标数据的bar，下层继承
		'''
		pass



	pass