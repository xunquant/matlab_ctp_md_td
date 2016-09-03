# -*- coding: utf-8 -*-
from os import path

if __name__ == '__main__':

	from program_top.utilities.process_and_main_function.main_function import main
	from program_top.components.standalone_working_class.process_manager import process_manager

	current_start_script=path.realpath(__file__)#取得当前main.py脚本的绝对路径
	main(current_start_script, process_manager)#传入单个工作实例的类定义，在主线程中构造之
	pass