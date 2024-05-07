# coding: UTF-8

#pylint:disable=C0209
#pylint:disable=C0411
#pylint:disable=C0413

"""
入口文件
"""

# 环境判断
try:
    from platform import python_implementation
except ImportError: # pragma: no cover
    import sys
    import os
    def python_implementation():
        """Return a string identifying the Python implementation."""
        if 'PyPy' in sys.version:
            return 'PyPy'
        if os.name == 'java':
            return 'Jython'
        if sys.version.startswith('IronPython'):
            return 'IronPython'
        return 'CPython'

implementation = python_implementation()

if implementation != "CPython":
    raise EnvironmentError("Unable to execute uel with %s" % (implementation,))

from uel.core.Main import Main
from sys import argv

if __name__ == "__main__":
    Main().main(argv)
