#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Let's compile UEL.
"""

# pylint:disable=W0621
# pylint:disable=W0212

try:
    import Cython as _
    import python_minifier as _
except:
    import pip
    
    pip.main(["install", "Cython", "python-minifier"])

from Cython.Build import cythonize

from os import cpu_count

from setuptools import setup
from setuptools import Extension
from setuptools import find_namespace_packages

from setuptools.command.build_ext import build_ext
from setuptools._distutils import file_util
from setuptools._distutils.errors import DistutilsFileError

from setuptools.dist import Distribution

import os
import sys
import re
import platform
import contextlib
import io
import python_minifier


def copy_file_contents(src, dst, buffer_size=16 * 1024):  # noqa: C901
    """Copy the file 'src' to 'dst'; both must be filenames.  Any error
    opening either file, reading from 'src', or writing to 'dst', raises
    DistutilsFileError.  Data is read/written in chunks of 'buffer_size'
    bytes (default 16k).  No attempt is made to handle anything apart from
    regular files.
    """
    # Stolen from shutil module in the standard library, but with
    # custom error-handling added.
    def _handler(data, file):
        if file.endswith(".py"):
            if "nominify" in os.path.split(file)[0]:
                return data
            return python_minifier.minify(data.decode(),
                remove_literal_statements=True,
                rename_globals=True).encode()
        return data
    
    fsrc = None
    fdst = None
    try:
        try:
            fsrc = open(src, 'rb')
        except OSError as e:
            raise DistutilsFileError(f"could not open '{src}': {e.strerror}")

        if os.path.exists(dst):
            try:
                os.unlink(dst)
            except OSError as e:
                raise DistutilsFileError(f"could not delete '{dst}': {e.strerror}")

        try:
            fdst = open(dst, 'wb')
        except OSError as e:
            raise DistutilsFileError(f"could not create '{dst}': {e.strerror}")
        
        src_data = _handler(fsrc.read(), src)
        fdst.write(src_data)
    
    finally:
        if fdst:
            fdst.close()
        if fsrc:
            fsrc.close()

with open("src/uel/nominify/version.py", "rt", encoding="utf8") as f:
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
        # self.parallel = False  # 并行编译虽然速度快了，但是错误信息不容易看
        self.parallel = True # 实在是太慢了


def check_environment():
    if platform.python_implementation() != "CPython" \
            or sys.version_info < (3, 11, 0):
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

    BUILD_DIR = "build/uel"
    INCLUDE = ["src/uel/include/"]

    C_COMPILE_ARGS = ["--std=gnu11"]
    CPP_COMPILE_ARGS = ["--std=gnu++17"]

    extensions.extend(cythonize(
        module_list=[
            Extension(
                name="uel.libary.sequence.module",
                sources=["src/uel/libary/sequence/module.pyx"]
            ),
            Extension(
                name="uel.ueargparse",
                sources=["src/uel/ueargparse.pyx"]
            )
            
        ],
        build_dir=BUILD_DIR,
        nthreads=os.cpu_count(),
        language_level="3str"
    ))

    extensions.extend([
        Extension(
            name="uel.bytecodefile._compress",
            sources=[
                "src/uel/bytecodefile/_compress.c",
                "src/uel/puel/dev-utils.c"
            ],
            include_dirs=INCLUDE,
            language="c",
            extra_compile_args=C_COMPILE_ARGS
        ),
        Extension(
            name="uel.impl.sequence",
            sources=[
                "src/uel/impl/sequence/sequence.c",
                "src/uel/puel/dev-utils.c"
            ],
            include_dirs=INCLUDE,
            language="c",
            extra_compile_args=C_COMPILE_ARGS
        )
    ])

    extensions.sort(key=lambda ext: sum(map(os.path.getsize, ext.sources)))

    return extensions

def is_minify():
    if len(sys.argv[1:]) > 1:
        return True
    if "dist" in sys.argv[1]:
        return True
    return False


kwargs = {
    "install_requires": ["objprint"]


}


metadata = dict(
    name = "uel",
    version = version,
    author = "XingHao. Li<3584434540@qq.com>",
    packages = find_namespace_packages("src"),
    package_dir = {
        "": "src"
    },
    package_data = {
        "uel": ["py.typed", "web/**"]
    },
    cmdclass = {
        "build_ext": UELParallelBuildExtension,
    },
    install_requires=["objprint"],
    entry_points = {
        'console_scripts': [
            'uel = uel.cli:main',
        ]
    },
)

check_environment()

if is_building():
    metadata["ext_modules"] = get_extensions()

if is_minify():
    file_util._copy_file_contents = copy_file_contents

setup(**metadata)
