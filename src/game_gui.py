from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
from game_base import Game
from robot import Robot
import debug as deb
import time

the_time = 0
the_cont = 0

class Liaison(QObject):

	def __init__(self,parent = None,n = 15,m = 15):
		super().__init__(parent = parent)
		self._game = Game(n,m)
		self._game.out_winner_info = False

	@pyqtSlot(int,int,result = int)
	def ask_cb(self,i,j):
		return self._game.chessboard.data[i][j]

	@pyqtSlot(int,int)
	def move(self,i,j):
		if(deb.flag1):
			global the_time
			global the_cont
			print ()
			print ("------------")

			print ("time : %f" % (time.clock() - the_time))
			the_time = time.clock()

			print ("cont1 = %d" % (deb.cont1))
			print ("cont2 = %d" % (deb.cont2))
			print ("cont3 = %d" % (deb.cont3))

			print ("------------")
			print ()
			deb.cont1 = 0
			deb.cont2 = 0
			deb.cont3 = 0

		self._game.move(i,j)

	@pyqtSlot(result = int)
	def ask_now(self):
		if(not self._game):
			return -1
		return self._game.now

	@pyqtSlot(result = QPoint)
	def get_robot_move(self):
		rb = Robot(self._game)
		res = rb.get_a_move()
		return QPoint(res[0],res[1])

	@pyqtSlot(int,int,result = bool)
	def is_good(self,i,j):
		return self._game.good(i,j)

	@pyqtSlot(result = int)
	def winner(self):

		if(self._game.over):
			return self._game.now
		return -1

	@pyqtSlot(result = int)
	def now_time(self):
		return self._game.now_time

	@pyqtSlot(result = QPoint)
	def last_move(self):
		res = self._game.last_move
		return QPoint(res[0],res[1])



path = 'main.qml'
app = QGuiApplication([])
view = QQuickView()
view.setTitle("五子棋")
lia = Liaison(n = 15,m = 15)

cont = view.rootContext()
cont.setContextProperty("lia", lia)

view.engine().quit.connect(app.quit)

view.setSource(QUrl(path))
view.show()
app.exec_()