'''
	debug版本的game_gui
	就是在初始化的时候预先走一些棋子而已（用来调试一些特殊情况）
'''
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQuick import *
from game_base import Game
from robot import Robot

def make_chess(s,i,j):
    s._game.move(i,j)

class Liaison(QObject):

    def __init__(self,parent = None,n = 15,m = 15):
        super().__init__(parent = parent)
        self._game = Game(n,m)
        self._game.out_winner_info = False

        make_chess(self,6,8)
        make_chess(self,7,5)
        make_chess(self,6,9)
        make_chess(self,10,6)
        make_chess(self,7,7)
        make_chess(self,8,8)
        make_chess(self,7,9)
        make_chess(self,9,6)
        make_chess(self,10,8)
        make_chess(self,9,7)
        make_chess(self,9,9)
        make_chess(self,8,9)



    @pyqtSlot(int,int,result = int)
    def ask_cb(self,i,j):
        return self._game.chessboard.data[i][j]

    @pyqtSlot(int,int)
    def move(self,i,j):
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
        print (self._game.now)

        if(self._game.over):
            return self._game.now
        return -1


    '''
    @pyqtSlot(int,int,re
    def check_
    '''

path = 'main.qml' 
app = QGuiApplication([])
view = QQuickView()
lia = Liaison(n = 15,m = 15)

cont = view.rootContext()
cont.setContextProperty("lia", lia)

view.engine().quit.connect(app.quit)

view.setSource(QUrl(path))
view.show()
app.exec_()