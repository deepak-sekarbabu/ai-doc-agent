# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for AI Documentation Agent

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('.')), 'src'))

block_cipher = None

a = Analysis(
    ['../src/ai_agent.py'],
    pathex=['../src'],
    binaries=[],
    datas=[
        ('../config/.env.example', 'config'),
        ('../src/doc_generator.py', '.'),
        ('../src/__init__.py', '.'),
    ],
    hiddenimports=[
        'requests',
        'dotenv',
        'markdown',
        'pdfkit',
        'doc_generator',
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ai-doc-agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
