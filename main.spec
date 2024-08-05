# main.spec

import sys
import os
from PyInstaller.utils.hooks import collect_all, copy_metadata

sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

# Collect all dependencies for streamlit
streamlit_data = collect_all('streamlit')

# Define the analysis
a = Analysis(
    ['src/main.py'],
    pathex=['/Users/rymac/PycharmProjects/CapstoneProject-Outkits'],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('config', 'config'),
        ('common', 'common'),
        ('venv/lib/python3.11/site-packages/streamlit/runtime', 'runtime'),
        *streamlit_data[0],  # Add the collected data from streamlit
    ],
    hiddenimports=[
        'openpyxl.cell._writer',
        'xlsxwriter',
        'streamlit.runtime.scriptrunner.magic_funcs'
    ],
    hookspath=[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
