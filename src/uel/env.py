import sys
from platform import python_implementation
from uel.cpython.py_excepthook import install


def check_and_install_excepthook():
    implementation = python_implementation()

    if not implementation == "CPython" or not sys.version_info >= (
        3, 10, 0
    ):
        raise OSError("UEL requires CPython 3.10+")

    install()
