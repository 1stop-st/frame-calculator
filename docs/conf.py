import sys
from os import path
import sphinx.apidoc

current_dir = path.abspath(path.dirname(__file__))
parent_dir = path.normpath(path.join(current_dir, '..'))
sys.path.append(parent_dir)

def run_apidoc(_):
    """Create (update) API documents automatically before generating pages."""
    pkgpath = path.join(parent_dir, 'frame_calculator')
    apipath = path.join(current_dir, 'apidocs')
    sphinx.apidoc.main([None, '-e', '--force', '-o', apipath, pkgpath])

def setup(app):
    app.connect('builder-inited', run_apidoc)

# Any Sphinx extension module names, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

# Any paths that contain templates, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# Could be a list. ex) source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'frame-calculator'
copyright = u'2017, 1stop-st.org'
author = u'1stop-st.org'

# The version info acts as replacement for |version| and |release|.
# The short X.Y version.
version = u'0.1'
# The full version, including alpha/beta/rc tags.
release = u'0.1.0'

# http://docs.sphinx-users.jp/config.html#confval-language
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# (Also effect to html_static_path and html_extra_path)
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# http://www.sphinx-doc.org/ja/stable/config.html#confval-html_theme
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': True
}

# Overwrite theme's default pygments style.
# pygments_style = 'sphinx'

# Any paths that contain custom static files (such as style sheets),
# relative to this directory.
# They will overwrite the builtin static files.
html_static_path = ['_static']

# Custom sidebar templates.
# http://www.sphinx-doc.org/ja/stable/config.html#confval-html_sidebars
# html_sidebars = {}
