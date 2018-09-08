一个用Python编写的沙雕五子棋AI，以及一个简陋的GUI<br>

------

* 运行:<br>

需要安装库PyQt5：
> pip install PyQt5

运行指令：
> python game_gui.py

或者（windows下）：
>start_game

------

* 构建：<br>

安装pyinstaller：
> pip install pyinstaller

之后运行指令
> pyinstaller -F -w game_gui.py -p analyzer.py -p analyzer_base.py -p chessboard.py -p debug_recursion.py -p game_base.py -p game_debug.py -p game_gui.py -p game_gui_debug.py -p robot.py -p score_base.py --hidden-import PyQt5.sip

或者（windows下）：
>make_file

------

* 代码复用：<br>
chessboard.py ：棋盘类<br>
analyzer.py & analyer_base.py ：分析器<br>
game_base.py ：游戏类<br>
robot.py & score_base.py ：AI<br>
game_gui.py & main.qml：游戏界面<br>
其他的基本上都是调试用文件<br>

类的依赖关系：<br>
Analyzer依赖Chessboard<br>
Game依赖Analyzer和ChessBoard<br>
Robot依赖Game、Analyzer和ChessBoard<br>

------

* 已知问题：<br>
4.1 太慢<br>
4.2 有的时候似乎会卡死<br>
4.2 <del>有的时候会变得智障</del>一直很智障<br>

------




