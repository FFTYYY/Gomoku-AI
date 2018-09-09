'''
主要包含一个五子棋分析器类（Analyzer）
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
	'''
		将棋盘的约定（用数字表示棋子）转化为分析器的约定（用字符串表示棋子）
		num表示棋盘上的符号
		now表示当前先手。

		棋盘约定：-1表示空格，非负数表示棋子，相同的数字来源于相同的玩家
		分析器约定："_"表示空格，"o"表示当前先手（即将落子者）棋子，"x"表示非当前先手棋子
	'''
	if(num == -1):
		return term.BLA
	elif(num == now):
		return term.NEX
	return term.PAS

FIX = term.PAS * 3

class Analyzer:
	'''
		五子棋的棋盘分析器
		应当在任意一个时刻创建，之后每在棋盘上落一个子，调用一次分析器的move()
		悔棋应调用分析器的unmove()并传入悔棋的位置（必须是上一次走的位置，否则会出现Bug）
	'''

	def __init__(self,chessboard = ChessBoard(0,0),nexa_range = 3):
		'''
			Analyzer的构造函数

			chessboard是棋盘
			nexa_range表示处理的相邻边界数量
		'''

		#要分析的棋盘
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

		'''
			这些是不同视角的棋盘
			其中hori表示行，vert表示列，main表示主对角线，vice表示副对角线

			每种视角，是一个有两个成员的列表，分别表示玩家0的视角和玩家1的视角
			每个成员是矩阵，矩阵的成员是字符串。成员编号规则见上面的注释

			注意分析器是按行处理的，所以行和列是两种不同的视角
		'''
		self._cb_hori = [[],[]]
		self._cb_vert = [[],[]]
		self._cb_main = [[],[]]
		self._cb_vice = [[],[]]

		#通过名称来查找视角
		self._cbs = {
			"行" 		: self._cb_hori,
			"列" 		: self._cb_vert,
			"主对角线" 	: self._cb_main,
			"副对角线" 	: self._cb_vice,
		}


		'''
			记录每个视角的棋盘的改变，以在恢复棋盘时使用
			每个成员是一个整数，表示第几行改变了，之后只需要重新分析这一行
		'''
		self._cb_hori_change = []
		self._cb_vert_change = []
		self._cb_main_change = []
		self._cb_vice_change = []
		#通过名称来查找棋盘改变
		self._cb_changes = {
			"行" 		: self._cb_hori_change,
			"列" 		: self._cb_vert_change,
			"主对角线" 	: self._cb_main_change,
			"副对角线" 	: self._cb_vice_change,
		}

		#名称列表
		self._cb_names = [o for o in self._cbs]

		'''

			nexa：记录贴近棋子中央的那些可落子点，即相邻（距离） <= nexa_range的格子集合
			距离定义为max(△x , △y)

			注意这些格子不一定是游戏中合法的可落子点，在真正落子的时候还要判断一下是否合法

			_nexa是一个栈，每次落子都会把这次落子点附近的点入栈，然后在_last_len中记录_nexa的长度，以便在回复时直接改变长度
		'''
		self._nexa_range = nexa_range
		self._nexa = []			#is a stack
		self._last_len = [0]
		#_dr：贴近棋子的可行的走法，即距离在nexa_range以内的所有走法列表
		self._dr = []

		'''
			上面是完成了一些成员的初始化
			调用init()函数来针对输入的棋盘完成一些操作
		'''
		self.init()


	def init(self):
		'''
			根据输入的棋盘，完成Analyzer()类的初始化
			这个函数只应该在Analyzer.__init__()中被调用
		'''

		#针对不同的玩家初始化他们看到的棋盘，并分析术语
		deal = [0,1]
		for i in deal:
			self.make_map(i)
			self.low_deal(i)

		#初始化走法
		for i in range(-self._nexa_range,self._nexa_range + 1):
			for j in range(-self._nexa_range,self._nexa_range + 1):
				self._dr.append((i,j))
		#初始化self._nexa
		self.make_nexa()


	def low_deal(self,now):
		'''
			基本的处理，判断每种情的况出现位置，存入_cases[now]中
			只应该在初始化的时候调用

			now表示当前考虑的玩家
		'''

		self._cases[now] = {}
		def make_deal(stri):
			for u in range(len(self._cbs[stri][now])):
				self.deal_line(stri,u,now)

		for name in self._cb_names:
			make_deal(name)

	'''
	def high_deal(self,now):
		#处理上层术语（术语树中非叶子的那些节点）
		#现在上层术语在cases_add()和cases_del()中处理，因此不需要这个函数了

		cases = self._cases[now]

		for i in term.cont_relat:
			cases[i] = []
			for j in term.cont_relat[i]:
				to_add = cases.get(j)
				if(to_add):
				cases[i] = cases[i] + to_add
	'''	

	def make_map(self,now):
		'''
			根据输入的棋盘来初始化成员，这个函数只应该在初始化的时候被调用
			或者是在debug时想要保证术语列表正确

			now表示当前要考虑的玩家编号（0或1）
		'''

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

	def make_nexa(self):
		'''
			初始化相邻落子点列表self._nexa
			这个函数只应该在初始化时被调用
			或者是在debug时想要保证nexa正确
			
		'''
		self._nexa = []

		while True:
			'''棋盘一个子都没有的情况'''
			cnt = 0
			for i in range(self._cb.n):
				for j in range(self._cb.m):
					if self._cb.data[i][j] >= 0:
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

	def cases_add(self,now,ter,what):
		'''
			往术语列表中添加一个元素

			now表示考虑的玩家
			ter表示术语名
			what表示要添加的术语的具体参数
		'''
		deb.cont1 += 1

		cases = self._cases[now]
		if(not cases.get(ter)):
			cases[ter] = []
		cases[ter].append(what)

		#传递到上层术语
		if(term.better.get(ter)):
			self.cases_add(now , term.better[ter] , what)

	def cases_del(self,now,ter,k):
		'''
			在术语列表中删除一个元素

			now表示考虑的玩家
			ter表示术语名
			k表示要删除的术语的位置
		'''

		cases = self._cases[now]

		the_one = cases[ter][k]

		if(not cases.get(ter)):
			return				#should throw a exception
		del cases[ter][k]

		#传递到上层述语
		if(term.better.get(ter)):
			new_ter = term.better[ter]

			if(the_one in cases[new_ter]):
				self.cases_del(now , new_ter , cases[new_ter].index(the_one))
 
	def del_line(self,stri,k,now):
		'''
			删除指定方向、指定行的某一行的术语
			调用这个函数后应立即调用deal_line()以更新术语列表

			stri是一个字符串，表示视角（行/列/主对角线/副对角线）
			k表示要处理的行号
			now表示考虑的玩家
		'''
		
		for _i in self._cases[now]:		#_i: 枚举术语名
			lis = self._cases[now][_i]	#lis: 本术语的元素列表

			for _j in range( len(lis)-1 , -1 , -1):		#_j: 枚举元素列表的下标
				_k = lis[_j]							#_k: 列表元素

				if(_k[0] == stri and _k[1] == k):		#删除第k行的元素
					self.cases_del(now , _i , _j)

	def deal_line(self,stri,k,now):
		'''
			更新某一行的术语
			注意这个函数只会增加_cases中的元素，不会删去不需要的，调用此函数之前应该先调用del_line()来删去原先的术语
			如果是在初始化的时候调用就不需要预先删去

			stri是一个字符串，表示视角（行/列/主对角线/副对角线）
			k表示要处理的行号
			now表示考虑的玩家
		'''

		def do_match(s,stri,pos):
			'''
				这个函数在字符串中去寻找术语并添加进术语列表中

				s : 一个字符串，要处理的棋盘行
				stri : 当前匹配方向名称（横、纵、主对角线、副对角线）
				pos：在添加时附加的位置参数，对于阳线来说是行数/列数，对于阴线来说是起始位置（即上文的k）
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
		'''
			将行视角的(i,j)转化为对应视角的坐标

			stri表示要转化的视角
			i,j表示行视角坐标
			返回一个元组表示期望的视角坐标
		'''

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
			raise Exception("Analyzer.ij_to_line_number() : invalid argument stri")

		return (p,q)

	def line_number_to_ij(self,stri,p,q):
		'''
			将某视角的坐标(p,q)转化为对应的行视角坐标

			stri表示要转化的视角
			p,q表示期望的视角坐标
			返回一个元组表示行视角坐标
		'''

		m = self._cb.m

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
			raise Exception("Analyzer.line_number_to_ij() : invalid argument stri")

		return (i,j)

	def update_nexa(self,i,j):
		'''
			走了(i,j)之后，更新nexa
			不删除已走格子，因为不多
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
			因为nexa是一个只增不减的栈，所以直接调整栈长度就行了
		'''

		if(len(self._last_len) < 2):
			raise Exception("Analyzer.unupdate_nexa() : bad call")

		self._last_len.pop()
		self._nexa = self._nexa[0 : self._last_len[-1]]

	def move(self,i,j,now):
		'''
			在棋盘上走一步，更新分析器
			注意这个函数并不会检查落子点合不合法，应当在调用之前检查

			i,j ： 落子位置
			now ： 落子方
		'''

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
		'''
			悔棋，恢复分析器状态。

			i,j：上一次走的位置
		'''
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
