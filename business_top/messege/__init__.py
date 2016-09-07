# -*- coding: utf-8 -*-

'''
消息类别
'''

subscribe={"event_type":"subscribe",#消息类别
		   "strategy_name":"",#策略名称
		   "strategy_machine":{'ip':"","port":""},#订阅者
		   "target_instrument":['ag1612','SR701']}#订阅的合约


unsubscribe={"event_type":"unsubscribe",
		   "strategy_name":"",
		   "strategy_machine":{'ip':"","port":""},
		   "target_instrument":['ag1612','SR701']}#取消订阅行情

subscribed={"event_type":"subscribed",#消息类别
		   "strategy_name":"",#策略名称
		   "strategy_machine":{'ip':"","port":""},#订阅者
		   "target_instrument":['ag1612','SR701']}#订阅的合约