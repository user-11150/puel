# coding: UTF-8

# pylint:disable=C0209
# pylint:disable=C0411
# pylint:disable=C0413
"""
入口文件
"""

import sys

from sys import exit
from uel.cli import main

assert sys.version_info >= (3, 0, 0)

if __name__ == "__main__":
    main()
    exit()
