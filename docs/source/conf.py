# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'UT-Austin Nuclear Progression Problems'
copyright = '2025, Cole Gentry'
author = 'Cole Gentry'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.mathjax',  # Enable math support with equation numbering
]

templates_path = ['_templates']
exclude_patterns = []

# Enable numbered figures, tables, and code-blocks
numfig = True
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Table %s',
    'code-block': 'Code Block %s',
    'section': 'Section %s'
}

# Math equation numbering
math_numfig = True
math_eqref_format = "Eq. {number}"



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Logo/Banner configuration
html_logo = '_static/banner.png'

# Custom CSS
html_css_files = [
    'custom.css',
]

