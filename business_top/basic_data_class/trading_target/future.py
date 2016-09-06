# -*- coding: utf-8 -*-

import re,pandas
from datetime import datetime,timedelta
from program_top.utilities import my_datetime
from business_top.basic_data_class.data_session_base.trading_data_series.bar_data_session import bar_data_session
from business_top.basic_data_class.trading_target import trading_target

class future(trading_target):
	def __init__(self, my_quant_trading_code, start_date=None, end_date=None):
		'''
		入参是一个两项的list，第一项为交易所代码，第二项为掘金的交易代码，有可能标准有可能非标准
		'''
		self.exchange_code=my_quant_trading_code[0]
		self.commodity_code=re.sub(r'\d','',my_quant_trading_code[1])#剔除其中的数字
		self.main_contract_coordinate=get_main_contract_coordinate(self.exchange_code, self.commodity_code, start_date, end_date)

		pass
	pass

class commodity_future(future):
	'''
	商品期货交易标的
	'''
	pass

class financial_future(future):
	'''
	金融期货交易标的，包含股指期货和国债期货
	'''
	pass


def get_main_contract_coordinate(exchange_code, contract_code, start_date=datetime.today().date(),end_date=datetime.today().date()):
	'''
	取得主力合约轴
	'''
	contract_list=[exchange_code+'.'+contract_code+each_month for each_month in get_contract_month_range(start_date, end_date, exchange_code)]
	contract_volumn_panel=pandas.DataFrame()#各个合约的成交量面板
	for each_contract in contract_list:
		current_series=get_contract_volume_series(each_contract, start_date, end_date)
		if current_series.__len__():
			contract_volumn_panel=pandas.concat([contract_volumn_panel, current_series], axis=1)
			contract_volumn_panel.rename(columns={'volume': each_contract}, inplace=True)#替换原来的列标签，每列是一个合约，每行一个交易日
			pass
		pass

	max_index_column=contract_volumn_panel.idxmax(1)
	return max_index_column


def get_contract_volume_series(contract_code,start_date=datetime.today().date(),end_date=datetime.today().date()):
	'''取得合约的成交量序列:exchange_code.contract'''
	current_data_session=bar_data_session(data_content_name=contract_code,session_start=start_date,session_end=end_date,data_period=timedelta(days=1))
	current_data_series=current_data_session.data_content_ref()

	if not current_data_series:#如果没有提取到数据，说明其实没有
		return current_data_series

	data_panel=pandas.DataFrame(current_data_series)
	time_stamps=data_panel['utc_time']
	new_timestamps=time_stamps.apply(my_datetime.posix_timestamp2datetime)
	data_panel.set_index(new_timestamps,inplace=True)
	return_data=data_panel['volume']
	return return_data

#取得合约的月份范围字符串列表
def get_contract_month_range(start_date,end_date,exchange_code='CZCE'):
	raw_month_list=[]
	start_month_date=my_datetime.get_month_1st_date(start_date)
	end_1st_day=my_datetime.get_month_1st_date(my_datetime.get_same_day_in_next_n_year(end_date))

	current_month_day=start_month_date

	while (True):
		current_month_str=current_month_day.strftime(my_datetime.date_contract_format)[2:]

		if exchange_code=='CZCE':#如果是郑商所品种，把年份前面的1再去掉
			current_month_str=current_month_str.capitalize()
		raw_month_list.append(current_month_str)

		if current_month_day>=end_1st_day:
			break

		current_month_day=my_datetime.get_same_day_in_next_n_month(current_month_day,1)
		pass

	return raw_month_list
