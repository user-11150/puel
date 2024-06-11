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

from concurrent.futures import ThreadPoolExecutor

from setuptools.dist import Distribution
import os
import time
import sys


def commandwrap(old):
    def new(self, command):
        print(f" {str(command)} ".center(get_col(), "="))
        old(self, command)
    return new


Distribution.run_command = commandwrap(Distribution.run_command)
THREADS = cpu_count() or 1

def get_col():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


class UELParallelBuildExtension(build_ext):
    def initialize_options(self, *args, **kwargs):
        super().initialize_options(*args, **kwargs)
        self.parallel = True

def is_building():
    if len(sys.argv) < 2:
        return True

    build_commands = ['build', 'build_py', 'build_ext', 'build_clib'
                      'build_scripts', 'install', 'install_lib',
                      'install_headers', 'install_scripts', 'install_data',
                      'sdist', 'bdist', 'bdist_dumb', 'bdist_rpm',
                       'check', 'bdist_egg', 'develop']
    return any(bc in sys.argv[1:] for bc in build_commands)


def get_extensions():
    extensions = []

    BUILD_DIR = "build/uel"

    # The cpp extensions compile args, don't contains Cython extension
    CUSTOM_CPP_BUILD_ARGS = ["--std=gnu++17"]

    # The c extensions compile args, don't contains Cython extension
    CUSTOM_C_BUILD_ARGS = ["--std=gnu11"]
    include = ["src/uel/include/"]
    extensions.extend(cythonize(
        [
            Extension(
                "uel.core.runner.Stack",
                sources=["src/uel/core/runner/Stack.pyx"]
            ),
            Extension(
                "uel.core.runner.Frame",
                sources=["src/uel/core/runner/Frame.pyx"]
            ),
            Extension(
                "uel.ueargparse",
                sources=["src/uel/ueargparse.pyx"]
            ),
            Extension(
                "uel.ue_web.ueweb",
                sources=["src/uel/ue_web/ueweb.pyx"]
            )
        ],
        build_dir=BUILD_DIR,
        nthreads=THREADS,
        language_level="3str"
    ))
    extensions.append(
        Extension(
            "uel.bytecodefile._compress",
            sources=["src/uel/bytecodefile/_compress.cpp"],
            language="cpp",
            depends=[
                *include
            ],
            include_dirs=include,
            extra_compile_args=CUSTOM_CPP_BUILD_ARGS
        )
    )
    return extensions


kwargs = {
    "install_requires": ["objprint"]
}


metadata = dict(
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
    install_requires=["objprint"],
    entry_points={
        'console_scripts': [
            'uel = uel.uel:main',
        ]
    },
)

if is_building():
    metadata["ext_modules"] = get_extensions()

setup(**metadata)
