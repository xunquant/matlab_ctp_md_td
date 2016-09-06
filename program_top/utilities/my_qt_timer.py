# encoding: UTF-8
from __future__ import division
from PyQt4.QtCore import QTimer,Qt

from datetime import datetime

class my_zmq_timer(object):
	'''
	根据zeromq的delayed_callback设计的定时器类
	'''
	def __init__(self,first_emit_moment=None,emit_interval=None,emit_function=None):
		'''
		首次调用时间：如果不指明，则一构造完毕就立即调用一次，如果指明，则必须为构造之后的某个时点，类型是datetime
		调用时间间隔：如果不指明，则为单次调用，以后再也不调用，如果指明，则每隔此时常调用一次，类型是timedelta
		调用函数：
		'''
		
	
	
	pass


class my_qt_timer(QTimer):
	def __init__(self,timeout_moment=None,timeout_task=None,repeat_interval=None,**kwargs):
		super(my_qt_timer, self).__init__()

		self.__on_time_task=timeout_task
		self._arguments=kwargs
		self.timeout.connect(self.time_out_task, Qt.QueuedConnection)

		if timeout_moment and timeout_task:#如果指定了要定时做什么任务，就绑定之
			self.setSingleShot(True)#单次触发

			if timeout_moment.__class__.__name__ != 'datetime':
				print '定时器输入类别应该为datetime'
				return
			current_moment=datetime.now()
			if current_moment>timeout_moment:
				print('定时器触发时刻已经在当前时刻之前')
				return
			from_now2timeout=timeout_moment-current_moment
			self.start(1000*from_now2timeout.total_seconds())
			pass

		if repeat_interval and timeout_task:#如果指定了重复周期
			self.setSingleShot(False)
			repeat_interval.total_seconds()
			self.start(repeat_interval.total_seconds()*1000)
			pass
		pass

	def time_out_task(self):
		next_time_parameter=self._arguments['kwargs']

		if next_time_parameter:
			self.__on_time_task(next_time_parameter)
		else:
			self.__on_time_task()

		pass
	pass