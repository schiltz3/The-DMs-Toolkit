# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import django

sys.path.insert(0, os.path.abspath(".."))
# sys.path.insert(0, os.path.abspath("../.."))
# sys.path.append("E:/git/The-DMs-Toolkit/toolkit/views/character_generator")
# sys.path.append("E:/git/The-DMs-Toolkit/toolkit/views/account")
# sys.path.append("E:/git/The-DMs-Toolkit/toolkit/views/saved/saved_loot")
os.environ["DJANGO_SETTINGS_MODULE"] = "thedmstoolkit.settings"
django.setup()
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "The DM's Toolkit"
copyright = "2022, Ronen Loundy, Jeffery Meverden, John Tabor, John Schiltz"
author = "Ronen Loundy, Jeffery Meverden, John Tabor, John Schiltz"
release = "o.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "migrations", ".\Tests"]
apidoc_excluded_paths = ["migrations", "Tests"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False
