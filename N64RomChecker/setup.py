import os
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

exe = Executable(
    script = 'N64RomChecker.py',
    base = base,
    icon = 'icons/n64.ico'
)

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'packages': ['os', 'sys', 're', 'tkinter'],
    'include_files': ['files/', 'icons/', 'images/', os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll')],
    'excludes': []
}

setup(
    name = 'N64 ROM Checker',
    version = '1.0',
    description = 'Display N64 ROMs Informations',
    author = 'PhantomNatsu',
    options = {'build_exe': options},
    executables = [exe]
)
