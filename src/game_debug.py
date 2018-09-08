import robot
import game_base
import debug as deb
import os
import pdb

s = game_base.Game(7,7)

def prin(s):
	print("now : %d" % s.now)
	deb.print_cb(s.chessboard)

def ask_player_move(s):
	while(True):
		st = input("now Player %d move : " % s.now)

		p = st.split(" ")
		if(len(p) > 1):
			i,j = int(p[0]),int(p[1])
		else:
			i = int(p[0])
			j = int(input())

		i -= 1
		j -= 1

		if(i < 0):
			break
		if(s.good(i,j)):
			break

	return (i,j)

def ask_robot_move(s):
	rb = robot.Robot(s)
	des = rb.get_a_move()
	return des

def de(s):
	deb.print_cases_dict (s._ana)


while(not s.over):

	prin(s)

	now = s.now

	if(now == 0 or now == 1):
		i,j = ask_player_move(s)
	else:
		i,j = ask_robot_move(s)

	if(i < 0 or j < 0):
		s.unmove()
	else:
		s.move(i,j)
	de(s)

