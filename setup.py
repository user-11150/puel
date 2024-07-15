#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Let's compile UEL.
"""

# pylint:disable=W0621
# pylint:disable=W0212

from Cython.Build import cythonize

from os import cpu_count

from setuptools import setup
from setuptools import Extension
from setuptools import find_namespace_packages

from setuptools.command.build_ext import build_ext

from setuptools.dist import Distribution

import os
import sys
import re
import platform

with open("src/uel/version.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
with open("README.md", "rt", encoding="utf8") as f:
    long_description = f.read()

THREADS = cpu_count() or 1


def get_col():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


class UELParallelBuildExtension(build_ext):
    def initialize_options(self, *args, **kwargs):
        super().initialize_options(*args, **kwargs)


def is_building():
    if len(sys.argv) < 2:
        return True

    build_commands = ['build', 'build_py', 'build_ext', 'build_clib'
                      'build_scripts', 'install', 'install_lib',
                      'install_headers', 'install_scripts', 'install_data',
                      'sdist', 'bdist', 'bdist_dumb', 'bdist_rpm', "bdist_wheel",
                       'check', 'bdist_egg', 'develop']
    return any(bc in sys.argv[1:] for bc in build_commands)


def get_extensions():
    extensions = []

    return extensions


kwargs = dict()

if is_building():
    kwargs["ext_modules"] = get_extensions()

setup(name = "uel",
    version = version,
    author = "XingHao. Li<3584434540@qq.com>",
    packages = find_namespace_packages("src"),
    long_description=long_description,
    long_desciption_type="text/markdown",
    package_dir = {
        "": "src"
    },
    package_data = {
        "uel": ["**"]
    },
    cmdclass = {
        "build_ext": UELParallelBuildExtension,
    },
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'uel = uel.cli:uel_main',
        ]
    },
    description="A programming language",
    keywords=["language", "uel", "puel", "programming"],
    **kwargs)
