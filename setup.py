#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Let's compile UEL.
"""

try:
    import Cython
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
            raise SystemExit
        else:
            print("I don't understand what you mean. Please enter your 'yes' or' no '.")

from Cython.Build import cythonize

from setuptools import setup
from setuptools import Extension
from setuptools import find_namespace_packages

kwargs = {
  "install_requires": ["objprint"]
}

BUILD_DIR = "build/uel"
THREADS = 5
OPTIMIZE = False
PYX_COMPILE_LANG = "c"

CPP_BUILD_ARGS = ["--std=c++11"]

extensions = [
    *cythonize(
        [
#            Extension(
#                "uel.modules.math.computer",
#                sources=["src/uel/modules/math/computer.pyx"],
#                language=PYX_COMPILE_LANG
#            )
             # 使用c extension会使打包速度变慢，进而影响开发速度，所以
             # UEL目前计划是以Python为主，python不行的话尽量优化算法，
             # 尽量不使用 c extension。
        ],
        build_dir=BUILD_DIR,
        nthreads=THREADS
    ),
    
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
    ext_modules=extensions,
    install_requires=["objprint"],
    entry_points={
        'console_scripts': [
            'uel = uel.uel:main',
        ]
    },
)

