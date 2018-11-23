pyinstaller -F -w game_gui.py -p analyzer.py -p analyzer_base.py -p chessboard.py -p debug_recursion.py -p game_base.py -p game_debug.py -p game_gui.py -p game_gui_debug.py -p robot.py -p score_base.py --hidden-import PyQt5.sip
rename dist\game_gui.exe Gomoku.exe
copy main.qml dist\main.qml
copy config.ini dist\config.ini
