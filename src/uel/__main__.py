# coding: UTF-8

#pylint:disable=C0209
#pylint:disable=C0411
#pylint:disable=C0413

"""
入口文件
"""
import sys

assert sys.version_info >= (3, 0, 0)

from uel.cli import main
from sys import exit

if __name__ == "__main__":
    main()
    exit()
