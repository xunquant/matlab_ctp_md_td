# -*- coding: utf-8 -*-
import json
import os

from extensions.ctpGateway.ctpGateway import CtpMdApi, CtpTdApi
from extensions.ctpGateway.vtGateway import VtLogData
from business_top.ctp_md_forwarder.vt_gateway_new import VtGateway

class CtpGateway(VtGateway):
	"""CTP接口"""

	#----------------------------------------------------------------------
	def __init__(self, binding_ref, gatewayName='CTP'):
		"""Constructor"""
		super(CtpGateway, self).__init__(binding_ref, gatewayName)
		
		self.mdApi = CtpMdApi(self)	 # 行情API
		self.tdApi = CtpTdApi(self)	 # 交易API
		
		self.mdConnected = False		# 行情API连接状态，登录完成后为True
		self.tdConnected = False		# 交易API连接状态
		
		self.qryEnabled = False		 # 是否要启动循环查询
		self.connect()
		
		
	#----------------------------------------------------------------------
	def connect(self):
		"""连接"""
		# 载入json文件
		
		userID=self.binding_instance._business_config['account_id']
		brokerID=self.binding_instance._business_config['broker_id']
		password=self.binding_instance._business_config['passcode']
		mdAddress=self.binding_instance._business_config['ctp_md_front']+":"+self.binding_instance._business_config['port']
		
		# 创建行情和交易接口对象
		self.mdApi.connect(userID, password, brokerID, mdAddress)
	#----------------------------------------------------------------------
	def subscribe(self, subscribeReq):
		"""订阅行情"""
		self.mdApi.subscribe(subscribeReq)
		
	#----------------------------------------------------------------------
	def sendOrder(self, orderReq):
		"""发单"""
		return self.tdApi.sendOrder(orderReq)
		
	#----------------------------------------------------------------------
	def cancelOrder(self, cancelOrderReq):
		"""撤单"""
		self.tdApi.cancelOrder(cancelOrderReq)
		
	#----------------------------------------------------------------------
	def qryAccount(self):
		"""查询账户资金"""
		self.tdApi.qryAccount()
		
	#----------------------------------------------------------------------
	def qryPosition(self):
		"""查询持仓"""
		self.tdApi.qryPosition()
		
	#----------------------------------------------------------------------
	def close(self):
		"""关闭"""
		if self.mdConnected:
			self.mdApi.close()
		if self.tdConnected:
			self.tdApi.close()
		
	#----------------------------------------------------------------------
	def initQuery(self):
		"""初始化连续查询"""
		if self.qryEnabled:
			# 需要循环的查询函数列表
			self.qryFunctionList = [self.qryAccount, self.qryPosition]
			
			self.qryCount = 0		   # 查询触发倒计时
			self.qryTrigger = 2		 # 查询触发点
			self.qryNextFunction = 0	# 上次运行的查询函数索引
			
			self.startQuery()
	
	#----------------------------------------------------------------------
	def query(self, event):
		"""注册到事件处理引擎上的查询函数"""
		self.qryCount += 1
		
		if self.qryCount > self.qryTrigger:
			# 清空倒计时
			self.qryCount = 0
			
			# 执行查询函数
			function = self.qryFunctionList[self.qryNextFunction]
			function()
			
			# 计算下次查询函数的索引，如果超过了列表长度，则重新设为0
			self.qryNextFunction += 1
			if self.qryNextFunction == len(self.qryFunctionList):
				self.qryNextFunction = 0
	
	#----------------------------------------------------------------------
	def startQuery(self):
		"""启动连续查询"""
		self.binding_instance.register(EVENT_TIMER, self.query)
	
	#----------------------------------------------------------------------
	def setQryEnabled(self, qryEnabled):
		"""设置是否要启动循环查询"""
		self.qryEnabled = qryEnabled
	


