一个用Python编写的沙雕五子棋AI，以及一个简陋的GUI

------

#### 1. 运行：
需要安装库PyQt5：
> pip install PyQt5

运行指令：
> python game_gui.py

或者（windows下）：
>start_game

------

#### 2. 构建：
安装pyinstaller：
> pip install pyinstaller

之后运行指令
> pyinstaller -F -w game_gui.py -p analyzer.py -p analyzer_base.py -p chessboard.py -p debug_recursion.py -p game_base.py -p game_debug.py -p game_gui.py -p game_gui_debug.py -p robot.py -p score_base.py --hidden-import PyQt5.sip

或者（windows下）：
>make_file

------

#### 3. 代码复用：
chessboard.py ：棋盘类
analyzer.py & analyer_base.py ：分析器
game_base.py ：游戏类
robot.py & score_base.py ：AI
game_gui.py & main.qml：游戏界面
其他的基本上都是调试用文件

类的依赖关系：
Analyzer依赖Chessboard
Game依赖Analyzer和ChessBoard
Robot依赖Game、Analyzer和ChessBoard

------

#### 4. 已知问题：
#####&emsp;4.1 太慢
#####&emsp;4.2 有的时候似乎会卡死
#####&emsp;4.2 <del>有的时候会变得智障</del>一直很智障

------




