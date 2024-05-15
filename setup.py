#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Let's compile UEL.
"""

from setuptools import setup

kwargs = {
  "install_requires": ["objprint"]
}

setup(
    name="uel",
    packages={
      "uel": "uel/"
    },
    package_data={
      "uel": ["py.typed"]
    },
    install_requires=["objprint"]
)

