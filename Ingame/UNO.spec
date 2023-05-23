# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['UNO.py'],
    pathex=[C:\Users\01022\OneDrive\Documents\GitHub\Softwareengineering\Ingame\UNO.py],
    binaries=[],
    datas=[('.\\image\\card_img\\*.png', 'image\\card_img'), ('.\\image\\map_image\\*.png', 'image\\map_image'), ('.\\image\\playing_image\\*.png', 'image\\playing_image'), ('.\\image\\setting_image\\*.png', 'image\\setting_image'), ('.\\image\\title_image\\*.png', 'image\\title_image'), ('.\\sound\\*.mp3', 'sound'), ('.\\*.py', '.')],
    hiddenimports=['sys', 'pygame', 'settings', 'constants', 'game_functions', 'loadcard.*', 'os', 'pickle', 'socket', 'network', 'server', 'client', 'rect_functions'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='UNO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
     windowed=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['unobutton.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UNO',
)
