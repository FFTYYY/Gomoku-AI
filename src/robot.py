from chessboard import ChessBoard
import copy
import score_base
import debug as deb
import time
import math
import random

'''
	TODO:
	现在的问题是，如果接下来几步双方都可以走出5（即都有四，但是实际上某一方是有绝对优势的），那么他不会认为自己的5是绝对优势。
	方案：在走出绝对优势后，立刻结束搜索。
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
		在落子后以落子为当前方进行局面评估

		判断该当前棋盘上哪一方更占优势
		cb表示当前棋盘，now表示当前先手（刚刚落子）
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
	return a[now] - a[now ^ 1]
def get_score(game):
	scr = score(game)
	scr = get_scr(scr,game.now)
	return scr

def get_sons(game):
	ret = [p for p in game._ana.get_nexa() if (game.good(p[0],p[1]))]
	deb.cont3 += len(ret)
	return ret


#deber = deb.deber

def dfs(game,depth = 0):

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

	def __init__(self,game):

		self._game = game
		self._root = None
		self._desicion = (0,0)


	def get_env(self):
		get_inv(self._game.now_time)

	def get_a_move(self):

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


