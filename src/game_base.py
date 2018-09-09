'''
	包含游戏类Game
'''

from chessboard import ChessBoard
from analyzer import Analyzer
import os
import copy
import debug as deb

class Game:

	def __init__(self,n = 15,m = 15):
		'''
			初始化一个游戏

			n,m：棋盘的长宽
		'''

		#棋盘
		self._cb = ChessBoard(n,m)

		#当前先手
		self._now = 0

		#禁止走的位置，对于每个玩家而言是一个棋盘，棋盘上非-1的位置即是不能走的
		self._bad = [ChessBoard(n,m) for _i in [0,1]]

		#棋盘长宽
		self._n = n
		self._m = m

		#分析器
		self._ana = Analyzer(self._cb , nexa_range = 1)

		#是否已经有人胜利了
		self._got_winner = False

		#是否检查胜利
		self._do_check_winner = True	
		#是否在控制台输出胜利信息
		self._out_winner_info = True

		#当前走了多少步
		self._now_steps = 0
		#之前走过的所有步骤
		self._last_moves = []
		#上一次走的位置
		self._last_move = None

		

	def good(self,i,j,now = -1):
		'''
			走(i,j)是可以的吗？
			 (now = -1 意味着now默认为self._now)
		'''
		if(now == -1):
			now = self._now
		flag = True
		flag = flag and i >= 0 and i < self._cb.n
		flag = flag and j >= 0 and j < self._cb.m
		flag = flag and self._bad[now][i][j] < 0
		return flag

	def move(self,i,j):
		'''
			在(i,j)这个位置落子
			前提是(i,j)是合法的，这个函数不会做检查

			i,j：落子位置
		'''

		self._cb[i][j] = self._now

		for _i in [0,1]:
			self._bad[_i][i][j] = 1
		self._last_move = (i,j)
		self._last_moves.append((i,j))
		self._now_steps += 1

		self._ana.move(i,j,self._now)

		if(self._do_check_winner and self.check_winner()):
			self.win()

		self._now ^= 1

	def unmove(self):
		'''
			悔棋
		'''

		self._now ^= 1

		self._got_winner = False

		self._ana.unmove(self._last_move[0] , self._last_move[1])

		i,j = self._last_moves.pop()

		if(len(self._last_moves) > 0):
			self._last_move = self._last_moves[-1]
		else:
			self._last_move = None

		for _i in [0,1]:
			self._bad[_i][i][j] = -1

		self._now_steps -= 1
		
		self._cb[i][j] = -1

	def get_analyzer(self):
		return self._ana

	def check_winner(self):
		return self._ana.ask_number("五",self._now) > 0

	def win(self):
		if(not self._do_check_winner):
			return
		if(self._out_winner_info):
			print("u win") 
		self._got_winner = True

	@property
	def chessboard(self):
		return self._cb

	@chessboard.setter
	def chessboard(self,val):
		self._cb.data = val

	@property
	def bad_points(self):
		return self._bad

	@bad_points.setter
	def bad_points(self,val):
		self._bad = val

	@property
	def now(self):
		return self._now

	@now.setter
	def now(self,val):
		self._now = val;

	@property
	def over(self):
		return self._got_winner

	@property
	def last_move(self):
		return self._last_move

	@property
	def do_check_winner(self):
		return self._do_check_winner

	@do_check_winner.setter
	def do_check_winner(self,val):
		self._do_check_winner = val

	@property
	def out_winner_info(self):
		return self._out_winner_info

	@out_winner_info.setter
	def out_winner_info(self,val):
		self._out_winner_info = val

	@property
	def now_time(self):
		return self._now_steps

if(__name__ == "__main__"):

	import debug

	s = Game(6,6)

	while(not s.over):
		os.system("cls")
		print("now : %d" % s.now)
		debug.print_cb(s.chessboard)

		i = 0
		j = 0
		while(True):
			i = int(input("now Player %d move : " % s.now)) - 1
			j = int(input("")) - 1
			if(s.good(i,j)):
				break
		
		s.move(i,j)






