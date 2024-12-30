# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
import os
import shutil
import time

# Get the absolute path to your assets
base_path = os.path.abspath('D:/phython projects/2048')
fonts_path = os.path.join(base_path, 'assets', 'fonts')
icon_path = os.path.join(base_path, 'assets', 'icon')
dist_path = os.path.join(base_path, 'src', 'dist')

# Clean up old build
if os.path.exists(dist_path):
    try:
        shutil.rmtree(dist_path)
        time.sleep(1)
    except:
        pass

a = Analysis(
    ['main.py'],
    pathex=[base_path],
    binaries=[],
    datas=[
        (os.path.join(fonts_path, 'Font Awesome 6 Free-Solid-900.otf'), 'assets/fonts'),
        (os.path.join(fonts_path, '04B_19.TTF'), 'assets/fonts'),
        (os.path.join(icon_path, '*'), 'assets/icon'),
        (os.path.join(base_path, '*.json'), '.')
    ],
    hiddenimports=[
        'win32timezone',
        'kivy.core.text',
        'kivy.core.window.window_sdl2',
        'kivy.core.window',
        'kivy.core.image',
        'pkg_resources.py2_warn',
        'email.parser',
        'email.utils',
    ],
    excludes=[
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'tkinter',
        'PySide2',
        'PyQt5',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'docutils',
        'IPython',
        'pydoc',
        'pdb',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)

# Remove unused modules but keep essential ones
a.binaries = [x for x in a.binaries if not x[0].startswith("mfc")]
a.binaries = [x for x in a.binaries if not x[0].startswith("pygame")]
a.binaries = [x for x in a.binaries if not x[0].startswith("tcl")]
a.binaries = [x for x in a.binaries if not x[0].startswith("tk")]

pyz = PYZ(a.pure, a.zipped_data, compress=True)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='2048',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip symbols to reduce size
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(icon_path, 'icon-512.ico'),
    version='file_version_info.txt'
)
