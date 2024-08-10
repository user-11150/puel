"""The UEL programing language"""

import sys

from platform import python_implementation

__all__: list[str] = []

implementation = python_implementation()

if not implementation == "CPython" or not sys.version_info >= (3, 10, 0):
    raise OSError("UEL requires CPython 3.10+")

from uel.cpython.py_excepthook import install

install()
