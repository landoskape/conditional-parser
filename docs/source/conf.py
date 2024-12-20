# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Conditional Parser"
copyright = "2024, Andrew T. Landau"
author = "Andrew T. Landau"
release = "0.0.2"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "argparse": ("https://docs.python.org/3/library/argparse.html", None),
}

html_context = {
    "display_github": True,
    "github_user": "landoskape",
    "github_repo": "conditional-parser",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}
