# -*- coding: utf-8 -*-

'''
调试
'''

def callback_debug_start():
	try:
		import pydevd
		pydevd.settrace(suspend=False, trace_only_current_thread=True)
	except:
		pass
	pass