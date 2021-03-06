#coding:utf-8

'''
	棋盘
'''

import copy

class ChessBoard:
	'''
		用来表示一个矩形棋盘（矩阵）的类
		n，m分别表示行数和列数
		棋盘的每个元素，-1表示空，0和1分别表示先后手的棋子
	'''

	def __init__(self,n,m):
		'''
			初始化
			
			n,m：期刊的行数、列数
		'''
		self._n = n
		self._m = m
		self._data = [[-1] * m for i in range(n)]

	@property
	def n(self):
		return self._n

	@property
	def m(self):
		return self._m

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self,val):
		self._data = val
		self._n = len(val)
		if(self._n == 0):
			self._m = 0
		else:
			self._m = len(val[0])

	def __getitem__(self,k):
		return self._data[k]

if(__name__ == "__main__"):
	a = ChessBoard(15,15)
	a[3][3] = 9
	print (a[3 : 5])
	print (a.m)
	a._m = 12
