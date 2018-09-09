import os
import debug_recursion

def print_cb(cb):
	s = []
	for i in range(cb.n):
		for j in range(cb.m):
			if(cb[i][j] == 0):
				s.append("○")
			elif(cb[i][j] == 1):
				s.append("×")
			else:
				s.append("口")
		s.append("\n")
	print ("".join(s))

def print_cb_game(game):
	print_cb(game.chessboard)


def get_a_game(a = 6,b = 6):
	import game_base
	s = game_base.Game(a,b)

	while(not s.over):
		os.system("cls")
		print("now : %d" % s.now)
		print_cb(s.chessboard)

		i = 0
		j = 0
		while(True):
			i = int(input("now Player %d move : " % s.now)) - 1
			j = int(input("")) - 1
			if(i < 0):
				break
			if(s.good(i,j)):
				break
		
		if(i < 0):
			break
		s.move(i,j)

	return s

def print_cases_dict(ana):
	dic = ana.cases_dict
	pp = 0
	for i in dic:
		print()
		print("now debuging %d" % pp)
		pp += 1
		for j in i:
			print ("{0} : ".format(j))
			for p in i[j]:
				print (p)


flag1 = True	#game_gui debug
flag2 = False
flag3 = False
flag4 = False	#robot debug
flag5 = False 	#analyzer.py : move()
flag6 = False
flag7 = False
cont1 = 0	#cases_add()
cont2 = 0	#make_nexa()
cont3 = 0	#robot.get_sons()
cont4 = 0
cont5 = 0
cont6 = 0
cont7 = 0

deber = debug_recursion.RecursionDebuger()

if __name__ == "__main__":
	print (get_a_game().chessboard.data)
