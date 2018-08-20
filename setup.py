#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable
"""
Plik tworzacy aplikacje dostepna w systemie Windows
"""
includes = ['./zs.png']
excludes = ['_gtkagg', '_tkagg']
packages = ['PySide', 'dzialki', 'main_window', 'zscal']
path = []

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(
    version='0.1',
    description=u'Program aktualizuje plik scal',
    name=u'ZScal',
    options = {"build_exe": {"include_files":includes,
                            "excludes":excludes,
                            "packages":packages,
                            "path":path
                            }
    },
    executables=[Executable('zscal.py', base=base,
                            targetName=u'zscal.exe', icon='./zs.ico')])


