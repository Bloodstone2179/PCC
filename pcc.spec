# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/Docs/Code/Code-Projects/AQA PseudoCode transpiler/main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Docs/Code/Code-Projects/AQA PseudoCode transpiler/compiler.py', '.'), ('D:/Docs/Code/Code-Projects/AQA PseudoCode transpiler/gcc.exe', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pcc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pcc',
)
