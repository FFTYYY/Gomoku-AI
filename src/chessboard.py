#coding:utf-8

'''
	棋盘
	n，m分别表示行数和列数
	-1表示空，0表示黑棋，1表示白棋
'''

import copy

class ChessBoard:
	
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

	def __init__(self,n,m):
		self._n = n
		self._m = m
		self._data = [[-1] * m for i in range(n)]

	def __getitem__(self,k):
		return self._data[k]

if(__name__ == "__main__"):
	a = ChessBoard(15,15)
	a[3][3] = 9
	print (a[3 : 5])
	print (a.m)
	a._m = 12
