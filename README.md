һ����Python��д��ɳ��������AI���Լ�һ����ª��GUI

------

####1. ���У�
��Ҫ��װ��PyQt5��
> pip install PyQt5

����ָ�
> python game_gui.py

���ߣ�windows�£���
>start_game

------

####2. ������
��װpyinstaller��
> pip install pyinstaller

֮������ָ��
> pyinstaller -F -w game_gui.py -p analyzer.py -p analyzer_base.py -p chessboard.py -p debug_recursion.py -p game_base.py -p game_debug.py -p game_gui.py -p game_gui_debug.py -p robot.py -p score_base.py --hidden-import PyQt5.sip

���ߣ�windows�£���
>make_file

------

####3. ���븴�ã�
chessboard.py ��������
analyzer.py & analyer_base.py ��������
game_base.py ����Ϸ��
robot.py & score_base.py ��AI
game_gui.py & main.qml����Ϸ����
�����Ļ����϶��ǵ������ļ�

���������ϵ��
Analyzer����Chessboard
Game����Analyzer��ChessBoard
Robot����Game��Analyzer��ChessBoard

------

####4. ��֪���⣺
#####&emsp;4.1 ̫��
#####&emsp;4.2 �е�ʱ���ƺ��Ῠ��
#####&emsp;4.2 <del>�е�ʱ���������</del>һֱ������

------




