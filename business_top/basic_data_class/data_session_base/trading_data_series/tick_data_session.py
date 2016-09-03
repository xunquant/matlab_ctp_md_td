# -*- coding: utf-8 -*-

import cPickle as pickle

import pandas
from gmsdk import md
from gmsdk.util import tick_to_dict

from program_top import stdafx
from program_top.basic_data_class import my_tick
from ..trading_data_series import trading_data_series

class tick_data_session(trading_data_series):#区段数据，有开始时间，结束时间，内容是tick数据，储存为pickle文件
	#把读取来的数据存成整段的文件，如果硬盘有就取出来，如果硬盘没有就用掘金接口提取出来，然后拼凑成策略层面要用的完整数据段

	def get_pickle_filename(self,target_contract,session_start,session_end):
		pickle_filename=stdafx.data_buffer_dir+'_'.join([target_contract, session_start.strftime(stdafx.my_datetime.data_buffer_time_format), session_end.strftime(stdafx.my_datetime.data_buffer_time_format), self.frequency])+'.pkl'
		return pickle_filename

	def extract_tick_data(self, session_start, session_end, target_contract):
		return_tick_dicts=[]
		ret_value=md.init("snake3342@qq.com","btbxl@121208")

		current_loop_start=session_start

		while(True):
			test_tick_list=md.get_ticks(target_contract, current_loop_start.strftime(stdafx.my_datetime.my_quant_time_format), session_end.strftime(stdafx.my_datetime.my_quant_time_format))
			if test_tick_list.__len__()<=1:#如果已经取不出数据，则跳出
				break
			current_final_tick=test_tick_list[test_tick_list.__len__()-1]
			current_final_tick_moment=stdafx.my_datetime.utc_float2datetime(current_final_tick.utc_time)
			current_loop_start=current_final_tick_moment#更新下一圈提数据的开始时刻
			test_tick_list.pop()
			return_tick_dicts.extend(test_tick_list)
			if current_loop_start>=session_end:#如果下圈开始时间已经等于最终时间，则结束
				break
			pass

		tick_series=[my_tick(tick_to_dict(each_tick)) for each_tick in return_tick_dicts]

		self.tick_profitability_walk(tick_series)
		my_tick_dict_series=[each.__dict__ for each in tick_series]

		pickle_filename=self.get_pickle_filename(target_contract,session_start,session_end)

		pickle_file=open(pickle_filename,mode='wb')
		pickle.dump(my_tick_dict_series,pickle_file,-1)
		pickle_file.close()
		return my_tick_dict_series

	def tick_profitability_walk(self,my_tick_series):
		for current_starting_index in range(my_tick_series.__len__()):#迭代每一个点作为起始点，看它是否是盈利段的起始点
			my_tick_series[current_starting_index].profitable_session_start=0

			for current_ending_index in range(current_starting_index+1, my_tick_series.__len__()):#迭代以当前起始点开始，之后的每个点，检查是否是做多盈利点
				ending_time=my_tick_series[current_ending_index].current_tick_moment.time()
				if (stdafx.my_datetime.trading_day_closing_prepare_time<=ending_time) and(ending_time<=stdafx.my_datetime.trading_day_closing_complete_time):#如果这个结束点已经介于在收盘前10秒，则不做判断，设定为不可盈利点(0)，继续看下面一个开始点
					break

				if my_tick_series[current_starting_index].s1_price>my_tick_series[current_ending_index].s1_price:#如果当前开始点确认不是做多盈利段的开始(接下来还有更低的多开点)
					my_tick_series[current_starting_index].profitable_session_start=0
					break
					pass

				if my_tick_series[current_starting_index].s1_price<my_tick_series[current_ending_index].b1_price:#如果当前开始点确认是一个做多盈利段的开始(一直没有出现更好的多开机会情况下出现了盈利的平多机会)
					my_tick_series[current_starting_index].profitable_session_start=1
					break
					pass
				pass

			if my_tick_series[current_starting_index].profitable_session_start==1:#如果本点已经确认是开多盈利点
				continue#跳入下一个开始点，不做空开检查
				pass

			for current_ending_index in range(current_starting_index+1, my_tick_series.__len__()):#迭代以当前起始点开始，之后的每个点，检查是否是做空盈利点

				ending_time=my_tick_series[current_ending_index].current_tick_moment.time()
				if (stdafx.my_datetime.trading_day_closing_prepare_time<=ending_time) and(ending_time<=stdafx.my_datetime.trading_day_closing_complete_time):#如果这个结束点已经介于在收盘前10秒，则不做判断，设定为不可盈利点(0)，继续看下面一个开始点
					break

				if my_tick_series[current_starting_index].b1_price<my_tick_series[current_ending_index].b1_price:#如果当前开始点确认不是做空盈利段的开始(即接下来还有更高的空开点)
					my_tick_series[current_starting_index].profitable_session_start=0
					break
					pass

				if my_tick_series[current_starting_index].b1_price>my_tick_series[current_ending_index].s1_price:#如果当前开始点确认是一个做空盈利段的开始(一直没有出现更好的空开机会情况下出现了盈利的平空机会)
					my_tick_series[current_starting_index].profitable_session_start=-1
					break
					pass
				pass
			pass#逐个开始点终结
		pass#函数终结

	def __init__(self,session_start,session_end,target_contract):
		super(tick_data_session, self).__init__(target_contract, session_start, session_end)

		self.frequency='tick'#tick类别的数据

		buffer_data=self._load_if_data_buffered(session_start, session_end, target_contract)

		if buffer_data is None:
			buffer_data=self.extract_tick_data(session_start, session_end, target_contract)
			pass

		my_tick_panel_frame=pandas.DataFrame(buffer_data)
		if not hasattr(my_tick_panel_frame,'current_tick_moment'):
			print session_start,session_end
			pass
		my_tick_panel_frame.set_index(pandas.DatetimeIndex(my_tick_panel_frame.current_tick_moment),inplace=True)#把时间戳设定为列标签
		my_tick_panel_frame.resample('500L')#重采样以500毫秒作为周期，数据向前填充
		self.data_panel=my_tick_panel_frame
		pass

	pass