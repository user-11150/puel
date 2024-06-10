#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Let's compile UEL.
"""

# pylint:disable=W0621

try:
    import Cython as _
except ImportError:
    import pip

    while True:
        print("You don't have cython installed,"
              "so you can't build UEL."
              "Do you want to install cython?")
        answer = input("(yes: install cython / no: no install cython)")
        if answer == "yes":
            print("Let's install cython!")
            pip.main(["install", "Cython"])
            break
        elif answer == "no":
            print("Quit")
            exit()
        else:
            print("I don't understand what you mean. Please enter your 'yes' or' no '.")


from Cython.Build import cythonize

from os import cpu_count

from setuptools import setup
from setuptools import Extension
from setuptools import find_namespace_packages

from setuptools.command.build_ext import build_ext
from setuptools.command.build import build

from setuptools.dist import Distribution
import os
import time


def commandwrap(old):
    def new(self, command):
        print()
        print(str(command).center(get_col(), "="))
        old(self, command)
    return new

Distribution.run_command = commandwrap(Distribution.run_command)

def get_col():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

class UELParallelBuildExtension(build_ext):
    def initialize_options(self, *args, **kwargs):
        super().initialize_options(*args, **kwargs)
        self.parallel = True

kwargs = {
    "install_requires": ["objprint"]
}

BUILD_DIR = "build/uel"

THREADS = cpu_count() or 1

# The cpp extensions compile args, don't contains Cython extension
CUSTOM_CPP_BUILD_ARGS = ["--std=c++14"]

# The c extensions compile args, don't contains Cython extension
CUSTOM_C_BUILD_ARGS = ["--std=c11"]

include = ["src/uel/include/"]


extensions = [
    *cythonize(
        [
            Extension(
                "uel.ue_web",
                sources=["src/uel/ue_web.pyx"]
            )
        ],
        build_dir=BUILD_DIR,
        nthreads=THREADS,
    ),
    Extension(
        "uel.bytecodefile._compress",
        sources=["src/uel/bytecodefile/_compress.cpp"],
        language="cpp",
        depends=[
            *include
        ],
        include_dirs=include
    )
]

setup(
    name="uel",
    packages=find_namespace_packages("src"),
    package_dir={
        "": "src"
    },
    package_data={
        "uel": ["py.typed", "web/**"]
    },
    cmdclass={
        "build_ext": UELParallelBuildExtension,
    },
    ext_modules=extensions,
    install_requires=["objprint"],
    entry_points={
        'console_scripts': [
            'uel = uel.uel:main',
        ]
    },
)
