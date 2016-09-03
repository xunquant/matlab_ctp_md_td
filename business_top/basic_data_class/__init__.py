# -*- coding: utf-8 -*-
import json


class basic_data_class(object):
	def __init__(self):
		self._data_content=None#数据内容本身，为一个pandas.series或者pandas.dataframe
		self._buffer_absolute_filename=''

	def _save_to_file(self,absolute_filename=None):
		'''将本实例的_data_content序列化并存入文件_buffer_absolute_filename'''
		if not absolute_filename:
			absolute_filename=self._buffer_absolute_filename

		saving_content=json.dumps(self._data_content)
		with open(absolute_filename,mode='w') as file_struct:
			file_struct.write(saving_content)
			file_struct.close()
			pass

		pass

	def _load_from_file(self,absolute_filename=None):
		'''把json文件中的数据读入_data_content'''
		if not absolute_filename:
			absolute_filename=self._buffer_absolute_filename

		with open(absolute_filename,mode='r') as file_struct:
			self._data_content=json.load(file_struct)
			file_struct.close()
			pass
		pass

	def data_content_ref(self):
		return self._data_content
	pass