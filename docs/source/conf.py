# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import time
import datetime
import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'UEL'
copyright = f'2024 - {time.strftime("%Y")}, Xinghao Li'
author = 'Xinghao Li'

release = 'unknown'
init_path = os.path.join(os.path.dirname(__file__), "..", "..", "src", "uel", "version.py")
with open(init_path) as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            release = line.split(delim)[1]
            break

print(release)

extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['tools/templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'sphinx_material'
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
html_additional_pages = {}
html_sidebars = {}

language = "en"

root_doc = "index"
