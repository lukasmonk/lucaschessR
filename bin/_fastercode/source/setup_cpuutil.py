from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from Cython.Build import cythonize

sourcefiles = ['CpuUtil.pyx', 'irina/cpu.c']

setup(ext_modules=cythonize([Extension("CpuUtil", sourcefiles, library_dirs=["."])]))
