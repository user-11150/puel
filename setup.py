#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from pkg_resources import require
except ImportError:
    raise ImportWarning("You need run \"python -m pip install setuptools\"") from None

require("setuptools", "Cython")

from Cython.Build import cythonize

from os import cpu_count

from setuptools import setup
from setuptools import Extension
from setuptools import find_namespace_packages

from setuptools.command.build_ext import build_ext

import re
import sys
import platform

with open("src/uel/version.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
with open("README.md", "rt", encoding="utf8") as f:
    long_description = f.read()

THREADS = cpu_count() or 1

class UELBuildExtension(build_ext):
    def initialize_options(self, *args, **kwargs):
        super().initialize_options(*args, **kwargs)
        self.parallel = True


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
    
    C_COMPILE_ARGS = ["--std=c11"]
    CPP_COMPILE_ARGS = ["--std=c++17"]
    
    
    extensions.extend([
        Extension(
            "uel.internal.uelcore_internal_exceptions",
            sources=["src/uel/internal/uelcore_internal_exceptions.c"]
        )
    ])

    return extensions

kwargs = dict()


if is_building():
    kwargs["ext_modules"] = get_extensions()
def t(m):
    try:
        return __import__(m)
    except:
        return False
setup(name = "uel",
    version = version,
    author="uel",
    author_email="3584434540@qq.com",
    packages = find_namespace_packages("src"),
    long_description=long_description,
    package_dir = {
        "": "src"
    },
    url="https://user-11150.github.io/puel",
    cmdclass = {
        "build_ext": UELBuildExtension,
    },
    package_data={
        "uel": ["**"]
    },
    install_requires=["executing"],
    entry_points = {
        'console_scripts': [
            'uel = uel.main:console_main',
        ]
    },
    description="A programming language",
    keywords=["language", "uel", "puel", "programming"],
    **kwargs)
