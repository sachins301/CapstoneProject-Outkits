# main.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['your_script.py'],
    pathex=['/path/to/your/project'],
    binaries=[],
    datas=[
        ('/Users/rymac/PycharmProjects/CapstoneProject-Outkits/resources', 'resources'),
        ('/Users/rymac/PycharmProjects/CapstoneProject-Outkits/config', 'config'),
        ('/Users/rymac/PycharmProjects/CapstoneProject-Outkits/common', 'common'),
        ('/Users/rymac/PycharmProjects/CapstoneProject-Outkits/venv/lib/python3.11/site-packages/streamlit/runtime', 'runtime')
    ],
    hiddenimports=[
        'openpyxl.cell._writer',
        'xlsxwriter',
        'streamlit.runtime.scriptrunner.magic_funcs'
    ],
    hookspath=['/Users/rymac/PycharmProjects/CapstoneProject-Outkits/hooks'],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
