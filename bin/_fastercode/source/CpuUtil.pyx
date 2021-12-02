# cython: language_level=2
cimport cython
import sys
import os.path
import os
import shutil
from libc.stdio cimport FILE

cdef extern from "irina.h":
    int is_bmi2()

def bmi2():
    return is_bmi2()