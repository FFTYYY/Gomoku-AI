'''
	五子棋机器人Robot类
'''

from chessboard import ChessBoard
import copy
import score_base
import debug as deb
import time
import math
import random
import pdb

'''
	TODO:太菜，需要更新dfs的剪枝策略
'''

deal_step_val = 3
deal_step = 3
deal_step_warn = 2
deal_step_cut = 1

cut_time_warn = 20
cut_time = 25

las_time = 0

remain_num = 15


def get_inv(now_time):
	'''
		调整一些全局变量
		其实不该是全局变量
		应该改改

		now_time是当前步数
	'''
	global remain_num
	remain_num = 20 - (now_time // 4)
	if(remain_num < 10):
		remain_num = 10

	global deal_range
	deal_range = 1 + (now_time // 15)
	if(deal_range > 3):
		deal_range = 3

_now_time = 0

def score(game,now = -1):
	'''
		给棋盘打分

		now表示当前先手（即将落子）方，返回的是一个元组，表示双方的分数
	'''

	if(now < 0):
		now = game.now
	ana = game.get_analyzer()

	scores = score_base.scores
	res = [0,0]

	def ask(no,str):
		nonlocal ana
		return ana.ask_number(str,no)

	for the_rules in scores:
			no = the_rules[0] ^ now
			the_name = the_rules[1]
			res[no] += ask(no,the_name) * scores[the_rules]

	return (res[0],res[1])

def get_scr(a,now):
	'''
		获得当前方分数

		a是score()返回的元组
		now是当前方
	'''
	return a[now] - a[now ^ 1]

def get_score(game):
	'''
		给一个游打分
	'''
	scr = score(game)
	scr = get_scr(scr,game.now)
	return scr

def get_sons(game):
	'''
		获得当前合法边界落子点集合
		game表示游戏
		用来当做机器人的尝试点
	'''
	#pdb.set_trace()

	ret = [p for p in game.get_analyzer().get_nexa() if (game.good(p[0],p[1]))]
	deb.cont3 += len(ret)

	if(deb.flag4):
		print (ret)
	return ret


#deber = deb.deber

def dfs(game,depth = 0):
	'''
		深度优先搜索

		game表示游戏
		depth表示当前深度，初始为0
	'''

	'''
	Debug

	global deber
	deber.set_point( (game.last_move) )
	info = {}
	info["last_move"] = game.last_move
	info["depth"] = depth
	info["now"] = game.now
	info["now_score"] = score(game)
	'''
	
	now = game.now

	got_five = False
	for _no in [0,1]:
		if(game.get_analyzer().ask_number("五",_no) > 0):
			got_five = True

	global las_time
	global deal_step

	now_time = time.clock() - las_time
	#if(now_time > cut_time_warn):
	#	deal_step = deal_step_warn
	if(now_time > cut_time):
		deal_step = deal_step_cut

	if depth >= deal_step or got_five:
		#info["return_val"] = (score(game) , (0,0))
		#deber.end_point(info)

		return (score(game) , (0,0))

	mov_lis = get_sons(game)

	def better(a,b):
		if not a:
			return b
		if not b:
			return a
		return get_scr(a , now) > get_scr(b , now)

	res = None
	res_step = None

	#筛选出排名靠前的move
	the_lis = []
	for mov in mov_lis:
		game.move(mov[0],mov[1])
		the_tuple = (get_score(game) , mov)
		game.unmove()
		the_lis.append(the_tuple)
	the_lis.sort(key = lambda t : t[0] , reverse = False)

	#print ([x[0] for x in the_lis])

	if(depth == 0 and deb.flag2):
		print ([x[0] for x in the_lis])


	to_cut = len(the_lis)
	for _i in range(len(the_lis)-1):

		the_rat = (the_lis[_i+1][0] + 0.0001) / (the_lis[_i][0] + 0.0001)
		the_dif = the_lis[_i+1][0] - the_lis[_i][0]
		if(the_rat < 1):
			the_rat = 1 / the_rat

		if((the_rat < 0 or the_rat >= 1.5) and the_dif > 5000):
			to_cut = _i
			if(depth == 0 and deb.flag2):
				print ("the_rat = %d" % (the_rat))
				print ("the_dif = %d" % (the_dif))
			break

	if(to_cut > remain_num):
		#random.shuffle(the_lis)
		to_cut = remain_num

	while(True):
		if(to_cut >= len(the_lis)):
			break
		if(the_lis[to_cut][0] == the_lis[to_cut-1][0]):
			to_cut += 1
		else:
			break
	if(to_cut < 1):
		to_cut = 1

	the_lis = the_lis[0: to_cut]
		
	if(depth == 0 and deb.flag2):
		print ([x[0] for x in the_lis])

	mov_lis = [tup[1] for tup in the_lis]

	for mov in mov_lis:
		
		game.move(mov[0],mov[1])

		ret = dfs(game , depth + 1)

		now_res = ret[0]

		if(better(now_res , res)):
			res = now_res
			res_step = mov
		game.unmove()

	#info["return_val"] = (res,res_step)
	#deber.end_point(info)

	return (res,res_step)

class Robot:
	'''
		机器人类

		因为数据都是在分析器中记录的，所以实际上可以对每一个游戏局面都创建一个新的机器人
	'''

	def __init__(self,game):
		'''
			机器人的初始化

			game表示这个机器人的游戏
		'''
		self._game = game
		self._root = None
		self._desicion = (0,0)


	def get_env(self):
		'''
			初始化全局变量
			我也不知道我在写些什么
			TODO
		'''
		get_inv(self._game.now_time)

	def get_a_move(self):
		'''
			请求机器人获得下一步走法
		'''

		self.get_env()

		global las_time
		global deal_step
		las_time = time.clock()
		deal_step = deal_step_val
		self._desicion = (dfs(self._game))[1]

		#global deber
		#deber.cui.exec_()

		return self._desicion


if(__name__ == "__main__"):

	import game_base

	p = ChessBoard(6,6)
	p.data =  [
		[ -1, -1, -1, -1, -1, -1,],
		[ -1, -1, -1, -1, -1, -1,],
		[ -1, -1,  0, -1, -1, -1,],
		[ -1, -1, -1, -1, -1, -1,],
		[ -1, -1,  0, -1,  1, -1,],
		[ -1, -1, -1, -1, -1, -1,],
	]

	g = game_base.Game(6,6)
	g._cb = p

	print (score(g))


