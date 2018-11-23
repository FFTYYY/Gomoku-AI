# -*- mode: python -*-

block_cipher = None


a = Analysis(['game_gui.py'],
             pathex=['analyzer.py', 'analyzer_base.py', 'chessboard.py', 'debug_recursion.py', 'game_base.py', 'game_debug.py', 'game_gui.py', 'game_gui_debug.py', 'robot.py', 'score_base.py', 'E:\\Programming\\Projects\\Doing\\Gomoku-AI\\src'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='game_gui',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
