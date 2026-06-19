# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件
用于打包 OmniDesk AI PyQt6 版本为 Windows EXE
"""

import sys
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent

block_cipher = None

a = Analysis(
    ['run_pyqt6.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        (str(project_root / 'assets'), 'assets'),
        (str(project_root / 'config.json'), '.'),
    ],
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtCharts',
        'backend.modules.ai_hot_reload',
        'backend.modules.agent_engine_complete',
        'backend.modules.security_audit_complete',
        'backend.modules.perception_engine_complete',
        'backend.modules.vm_manager',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
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
    name='OmniDesk-AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'assets' / 'images' / 'icon.ico'),
)

# 创建 Windows 安装程序
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OmniDesk-AI',
)
