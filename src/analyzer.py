#coding:utf-8

'''
术语：（来源：百度百科）
〖威胁〗下一手可以成五或者活四的点。

（情况编号）
（每种情况可以对应唯一的一个情况）
0〖连〗2枚以上的同色棋子在一条线上邻接成串
	1〖成五〗五连和长连的统称。
		2〖五连〗五枚同色棋子在一条线上邻接连串。
		3〖长连〗五枚以上同色棋子在一条线上邻接成串。

	4〖四〗五连去掉1子的棋型。
		5〖活四〗有两个威胁的四。
		6〖冲四〗只有一个威胁的四。
		7〖死四〗不能成五的四连。

	8〖三〗可以形成四再形成五的三枚同色棋子组成的棋型。
		9〖活三〗再走一着可以形成活四的三。
		10〖连活三〗两端都是威胁的活三。简称“连三”。
		11〖跳活三〗中间夹有一个威胁的活三。简称“跳三”。
		12〖眠三〗再走一着可以形成冲四的三。
		13〖死三〗不能成五的三。

	14〖二〗可以形成三、四直至五的两枚同色棋子组成的棋型。
		15〖活二〗再走一着可以形成活三的二。
		16〖连活二〗连的活二。简称“连二”。
		17〖跳活二〗中间隔有一个空点的活二。简称“跳二”。
		18〖大跳活二〗中间隔有两个空点的活二。简称“大跳二”。
		19〖眠二〗再走一着可以形成眠三的二。
		20〖死二〗不能成五的二。

'''

from chessboard import ChessBoard
import copy
import time
from analyzer_base import terms
import analyzer_base as term
import re
import debug as deb
import pdb


def number_to_char(num,now):
	if(num == -1):
		return term.BLA
	elif(num == now):
		return term.NEX
	return term.PAS

FIX = term.PAS * 3

class Analyzer:
	'''构造函数说明：第二个参数是棋盘，第三个参数是要处理的棋子颜色集合，其元素必须是0或者1'''

	def __init__(self,chessboard = ChessBoard(0,0),nexa_range = 3):
		'''
			chessboard是棋盘
			nexa_range表示处理的相邻边界数量
		'''

		self._cases = [{},{}]
		self._cb = chessboard

		'''
			_cases是一个包含两个字典的列表，分别针对黑子和白子
			每个元素是一个列表字典，按术语名查找匹配此术语的位置列表
				列表的每个元素是一个三元组，
					第一个元素表明方向（横、纵、主对角线、副对角线）
					第二个元素表明初始位置（对于阳线来说是行数/列数，对于阴线来说是编号，编号顺序为先纵后横，折点归为横）
						同一行棋盘的排列顺序原则是优先从上到下，其次从左到右
					第三个元素表明匹配位置，这是一个区间，表明在这个区间里面有一次匹配（注意这个区间有可能延伸到棋盘外，即有负数边界）

			注：阴线编号顺序：
			主：  				副：
			n-1 n n+1 ... 		n-1 n n+1 ... n+m-1
			0									0
			1									1
			...									...
			n-2									n-2

		'''
		self._cases = [{},{}]
		self._cb_hori = [[],[]]
		self._cb_vert = [[],[]]
		self._cb_main = [[],[]]
		self._cb_vice = [[],[]]
		self._cbs = {
			"行" 		: self._cb_hori,
			"列" 		: self._cb_vert,
			"主对角线" 	: self._cb_main,
			"副对角线" 	: self._cb_vice,
		}


		#change的格式：(位置)
		self._cb_hori_change = []
		self._cb_vert_change = []
		self._cb_main_change = []
		self._cb_vice_change = []
		self._cb_changes = {
			"行" 		: self._cb_hori_change,
			"列" 		: self._cb_vert_change,
			"主对角线" 	: self._cb_main_change,
			"副对角线" 	: self._cb_vice_change,
		}

		self._cb_names = [o for o in self._cbs]

		'''
			nexa：即相邻（距离） <= nexa_range的位置集合
			距离定义为max(△x , △y)

			注意这些行动不一定是游戏中合法的行动，在真正落子的时候还要判断一下是否合法
		'''
		self._nexa_range = nexa_range
		self._nexa = []			#is a stack
		self._last_len = [0]
		self._dr = []	#moves

		self.init()


	def init(self):

		deal = [0,1]
		for i in deal:
			self.make_map(i)
			self.deal(i)

		for i in range(-self._nexa_range,self._nexa_range + 1):
			for j in range(-self._nexa_range,self._nexa_range + 1):
				self._dr.append((i,j))

		self.make_nexa()

	def make_map(self,now):
		cb = self._cb

		#横向
		_cb_hori = []
		for i in range(cb.n):
			ss = []
			for j in range(cb.m):
				#print ((i,j,cb.n))
				ss.append(number_to_char(cb[i][j],now))
			_cb_hori.append(ss)

		#纵向
		_cb_vert = []
		for j in range(cb.m):
			ss = []
			for i in range(cb.n):
				ss.append(number_to_char(cb[i][j],now))
			_cb_vert.append(ss)
		
		#主对角线
		_cb_main = []
		for (r,t) in ( list(zip([0] * cb.m , range(0,cb.m))) + list(zip(range(1,cb.n) , [0] * (cb.n-1))) ):
			ss = []

			i,j = (r,t)
			while(True):
				ss.append(number_to_char(cb[i][j],now))
				i += 1
				j += 1
				if(i >= cb.n or j >= cb.m):
					break
			_cb_main.append(ss)

		#副对角线
		_cb_vice = []
		for (r,t) in (list(zip([0] * cb.m , range(0,cb.m)))) + list(zip(range(1,cb.n) , [cb.m-1] * (cb.n-1)) ):
			ss = []

			i,j = (r,t)
			while(True):
				ss.append(number_to_char(cb[i][j],now))
				i += 1
				j -= 1
				if(i >= cb.n or j < 0):
					break
			_cb_vice.append(ss)

		self._cb_hori[now] = _cb_hori
		self._cb_vert[now] = _cb_vert
		self._cb_main[now] = _cb_main
		self._cb_vice[now] = _cb_vice

	def cases_add(self,now,ter,what):
		deb.cont1 += 1

		cases = self._cases[now]
		if(not cases.get(ter)):
			cases[ter] = []
		cases[ter].append(what)

		if(term.better.get(ter)):
			self.cases_add(now , term.better[ter] , what)

	def cases_del(self,now,ter,k):
		cases = self._cases[now]

		the_one = cases[ter][k]

		if(not cases.get(ter)):
			return				#should throw a exception
		del cases[ter][k]

		if(term.better.get(ter)):
			new_ter = term.better[ter]

			if(the_one in cases[new_ter]):
				self.cases_del(now , new_ter , cases[new_ter].index(the_one))
 
	def deal_line(self,stri,k,now):
		'''
			处理某一行的添加
		'''
		def do_match(s,stri,pos):
			'''
				s : 生成的棋盘行
				stri : 当前匹配方向名称（横、纵、主对角线、副对角线）
				pos：位置参数，对于阳线来说是行数/列数，对于阴线来说是起始位置
			'''
			for c in terms:
				res = re.finditer(c,s);
				if(res):
					for it in res:
						m_a,m_b = it.span()
						m_a -= len(FIX)
						m_b -= len(FIX)

						to_add = (stri , pos , (m_a,m_b))		#要加入的cases底层元素
						self.cases_add(now , terms[c] , to_add)


		ss = self._cbs[stri][now][k]
		s = FIX + ("".join(ss)) + FIX
		do_match(s,stri,k)

	def ij_to_line_number(self,stri,i,j):
		#n = self._cb.n
		m = self._cb.m

		if(stri == "行"):
			p,q = i,j
		elif(stri == "列"):
			p,q = j,i
		elif(stri == "主对角线"):
			q = min(i,j)

			if(i > j):
				p = i-j+m-1
			else:
				p = j-i
		elif(stri == "副对角线"):
			p,q = (i+j),min(i,m-j-1)
		else:
			return (-1,-1)
		#print (stri)
		return (p,q)

	def line_number_to_ij(self,stri,p,q):
		#n = self._cb.n
		m = self._cb.m

		#deb.cont += 1

		if(stri == "行"):
			i,j = p,q
		elif(stri == "列"):
			i,j = q,p
		elif(stri == "主对角线"):
			if(p >= m):
				i = p+q-m+1
				j = q
			else:
				i = q
				j = p+q

		elif(stri == "副对角线"):
			if(p >= m-1):
				i = p+q+1-m
			else:
				i = q
			j = p-i
		else:
			return (-1,-1)
		return (i,j)

	def del_line(self,stri,p,now):
		'''删除指定方向、指定行的某一行的分析'''
		for _i in self._cases[now]:		#_i: 枚举术语名
			lis = self._cases[now][_i]	#lis: 本术语的元素列表

			for _j in range( len(lis)-1 , -1 , -1):		#_j: 枚举元素列表的下标
				_k = lis[_j]							#_k: 列表元素
				#print(_k)
				#deb.cont += 1
				if(_k[0] == stri and _k[1] == p):		#删除第p行的元素
					self.cases_del(now , _i , _j)


	def make_nexa(self):

		self._nexa = []

		while True:
			'''棋盘一个子都没有的情况'''
			cnt = 0
			for i in range(self._cb.n):
				for j in range(self._cb.m):
					cnt += 1

			if cnt == 0:
				if self._nexa_range > 0:
					self._nexa.append( (self._cb.n // 2 , self._cb.m // 2) )
					self._last_len.append(len(self._nexa))
					return 
			break

		cb = self._cb
		for i in range(cb.n):
			for j in range(cb.m):
				#尝试(i,j)

				for p in self._dr:
					deb.cont2 += 1

					ni,nj = i+p[0],j+p[1]

					if p[0] == 0 and p[1] == 0:
						continue

					#deb.cont += 1
					if(ni >= 0 and  ni < cb.n and nj >= 0 and nj < cb.m and cb[ni][nj] >= 0):
						self._nexa.append( (i,j) )
						break
		self._last_len.append(len(self._nexa))

	def update_nexa(self,i,j):
		'''
			走了(i,j)之后，更新nexa
			不删除已走格子了，因为不多
		'''

		#if (i,j) in self._nexa:
		#	self._nexa.remove((i,j))

		cb = self._cb
		for p in self._dr:
			ni,nj = i+p[0],j+p[1]

			deb.cont2 += 1
			if p[0] == 0 and p[1] == 0:
				continue

			#deb.cont += 1

			#去寻找(i,j)附近的合法空格子
			if(ni >= 0 and  ni < cb.n and nj >= 0 and nj < cb.m and cb[ni][nj] < 0):
				self._nexa.append( (ni,nj) )
		self._last_len.append(len(self._nexa))

	def unupdate_nexa(self,i,j):
		'''
			不走(i,j)这一步，回退nexa
			应当把(i,j)附近的不合法格子删去，并且看是否加入(i,j)
		'''

		if(len(self._last_len) < 2):
			raise Exception("Analyzer.unupdate_nexa() : bad call")

		self._last_len.pop()
		self._nexa = self._nexa[0 : self._last_len[-1]]


	def low_deal(self,now):
		'''基本的处理，判断每种情的况出现位置，存入_cases[now]中'''
		
		#pdb.set_trace()

		def make_deal(stri):
			for u in range(len(self._cbs[stri][now])):
				self.deal_line(stri,u,now)

		for name in self._cb_names:
			make_deal(name)
	'''
	def high_deal(self,now):
		高层次的处理，合并有包含关系的关键字
		cases = self._cases[now]

		for i in term.cont_relat:
			cases[i] = []
			for j in term.cont_relat[i]:
				to_add = cases.get(j)
				if(to_add):
					cases[i] = cases[i] + to_add
	'''	
	def deal(self,now):
		'''这个函数是初始化的处理，会保证清空情况数组'''
		self._cases[now] = {}
		self.low_deal(now)
		#self.high_deal(now)

	@property
	def cases_dict(self):
		return self._cases

	def ask(self,stri,now = 0):
		return self._cases[now].get(stri)

	def ask_number(self,stri,now = 0):
		the_case = self._cases[now].get(stri)
		if(not the_case):
			return 0
		return len(the_case)

	def move(self,i,j,now):
		'''now ： 落子方'''
		#print ("i = {0}".format(i))
		def make_change(stri):				
			'''
				改变棋盘，删除这些行旧的术语，调用deal_line()来添加新的术语
				stri: deal direction
			'''
			cb = self._cbs[stri]
			p,q = self.ij_to_line_number(stri,i,j)
			cb[now][p][q] = term.NEX
			cb[now^1][p][q] = term.PAS

			cb_change = self._cb_changes[stri]
			cb_change.append( (p,q) )

			for no in [0,1]:
				self.del_line(stri,p,no)
				self.deal_line(stri,p,no)

		for _i in self._cb_names:
			make_change(_i)

		self.update_nexa(i,j)
		#self.make_nexa()

	def unmove(self,i,j):
		def unmake_change(stri):				
			'''
				恢复棋盘的改变
				stri: deal direction
			'''
			cb = self._cbs[stri]
			cb_change = self._cb_changes[stri]

			p,q = cb_change.pop()

			for no in [0,1]:
				cb[no][p][q] = term.BLA
				self.del_line(stri,p,no)
				self.deal_line(stri,p,no)

		for _i in self._cb_names:
			unmake_change(_i)

		#self.make_nexa()
		self.unupdate_nexa(i,j)

	def get_nexa(self):
		'''接下来可以走的格子'''
		return self._nexa

if(__name__ == "__main__"):
	import debug
	st = time.clock()

	p = ChessBoard(6,8)
	p.data = [
		[ -1, -1, -1, -1, -1, -1, -1, -1,],
		[ -1, -1, -1, -1, -1, -1, -1, -1,],
		[ -1, -1, -1, -1, -1, -1, -1, -1,],
		[ -1, -1, -1, -1, -1, -1, -1, -1,],
		[ -1, -1, +1, -1, -1, -1, -1, -1,],
		[ -1, -1, -1, +1, -1, -1, -1, -1,],
	]

	a = Analyzer(p)


	debug.print_cb(p)
	print (a._nexa)


	ed = time.clock()
	print ("time = %f" % (ed - st))
