import os
import sys
sys.path.insert(0, os.path.abspath('../../python/pyKobayashiIso'))

project = 'Kobayashi Isotropic Directional Solidification'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
