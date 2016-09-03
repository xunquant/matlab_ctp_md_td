# -*- coding: utf-8 -*-

from program_top.utilities.process_and_main_function.my_engine import my_engine

def load_instances(current_environment_pack):
	'''这里负责启动所有要工作的进程'''

	current_working_instances={
		'ma_stupid_multi_contract':my_engine(ma_stupid_multi_contract,current_environment_pack)
			}


	return current_working_instances