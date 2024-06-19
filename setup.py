#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Let's compile UEL.
"""

# pylint:disable=W0621

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
import warnings

with open("src/uel/version.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

def commandwrap(old):
    def new(self, command):
        print(f" {str(command)} ".center(get_col(), "*"))
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
    
    def finalize_options(self):
        super().finalize_options()
        
        self.global_include_c_sources = []
        self.global_include_c_sources_dirs = []
        
        
        self.global_include_dirs = ["src/uel/include/"]
        
        for include_dir in self.global_include_c_sources_dirs:
            for root, dirs, files in os.walk(include_dir):
                for file in files:
                    if not file.endswith(".c"):
                        continue
                    self.global_include_c_sources.append(os.path.join(root, file))

    def build_extension(self, extension: Extension):
        extra_compile_args = ["--std=gnu11"]
        
        extension.sources.extend(self.global_include_c_sources)
        extension.depends.extend(self.global_include_c_sources)
        
        extension.depends.extend(self.global_include_dirs)
        
        extension.extra_compile_args.extend(extra_compile_args)
        extension.include_dirs.extend(self.global_include_dirs)
        
        extension.language = "c"
        
        super().build_extension(extension)

def check_environment():
    if platform.python_implementation() != "CPython" \
            or sys.version_info < (3, 7, 0):
        if platform.python_implementation() != "CPython":
            raise EnvironmentError("Python implementation must be CPython")
        else:
            raise EnvironmentError("Python version is too low")
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

    extensions.append(
        Extension(
            name="uel.bytecodefile._compress",
            sources=[
                "src/uel/bytecodefile/_compress.c",
                "src/uel/puel/dev-utils.c"
            ],
        ))
    return extensions


kwargs = {
    "install_requires": ["objprint"]
}


metadata = dict(
    name="uel",
    version=version,
    author="XingHao. Li<3584434540@qq.com>",
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
            'uel = uel.cli:main',
        ]
    },
)

check_environment()

if is_building():
    metadata["ext_modules"] = get_extensions()

setup(**metadata)
