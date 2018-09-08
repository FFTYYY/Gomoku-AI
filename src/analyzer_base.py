#coding:utf-8

'''
术语列表
'''

terms = {
	"o{6,}" :			"长连",
	"[x_]ooooo[x_]" :	"五连",

	"xoooo_" :			"冲四",
	"xooox" :			"死四",
	"_oooo_" :			"活四",

	"[x_]oo_oo[x_]" :	"冲四",
	"[x_]ooo_o[x_]" :	"冲四",

	"xooox" :			"死三",
	"xooo_x" :			"死三",
	"xoo_ox" :			"死三",

	"xooo__" :			"眠三",
	"x_ooo_x" :			"眠三",

	"x_ooo__" :			"活三",
	"__ooo__" :			"活三",

	"_oo_o_" :			"活三",

	"xoo_o_" :			"眠三",

	"[x_]o_o_o[x_]" :	"眠三",
	"[x_]oo__o[x_]" :	"眠三",

	"x_oo___" :			"活二",
	"__oo__" :			"活二",

	"x_o_o__" :			"活二",
	"__o_o__" :			"活二",

	"_o__o_" :			"活二",

	"xoo___" :			"眠二",
	"xo__o_" :			"眠二",
	"x_o_o_x" :			"眠二",
	"xo_o__" :			"眠二",
	"x_oo__x" :			"眠二",
	"[x_]o___o[x_]" :	"眠二",

	"xoox" :			"死二",
	"xoo_x" :			"死二",
	"xo_ox" :			"死二",
	"xoo__x" :			"死二",
	"xo_o_x" :			"死二",
	"xo__ox" :			"死二",
	"x_oo_x" :			"死二",
}

def deal():
	global terms

	terms_2 = {}

	for i in terms:
		j = i[::-1]
		jj = list(j)
		for k in range(len(jj)):
			if(jj[k] == "["):
				jj[k] = "]"
			elif(jj[k] == "]"):
				jj[k] = "["
		for k in range(len(jj)):
			if(k+1 < len(jj) and jj[k] == "x" and jj[k+1] == "]"):
				jj[k] = "_"
			if(k-1 >= 0 	 and jj[k] == "_" and jj[k-1] == "["):
				jj[k] = "x"
		j = "".join(jj)	

		if( (j != i) and (terms[i] != "长连") ):
			terms_2[j] = terms[i]
	terms.update(terms_2)

deal()

NEX = "o" #先手棋子
PAS = "x" #后手棋子
BLA = "_" #空白棋盘

cont_relat = {
	"二" : ["死二","眠二","活二",],
	"三" : ["死三","眠三","活三",],
	"四" : ["死四","冲四","活四",],
	"五" : ["五连","长连",],
}

#cont_relat的逆映射
better = {}

def deal_better():
	for _i in cont_relat:
		for _j in cont_relat[_i]:
			better[_j] = _i
deal_better()

if __name__ == "__main__":

	import re

	#for i in terms:
	#	print("{0} : {1}".format(terms[i],i))


	s1 = "xxx____oox___xxx"

	for i in terms:
		p = re.finditer(i,s1)
		if(p):
			for j in p:
				print ("{0} : {1}".format(j.span() , terms[i]))
