#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pip install https://github.com/jfbercher/IPython-notebook-extensions/archive/master.zip --user
#pip install git+https://github.com/jfbercher/IPython-notebook-extensions@master#egg=IPython-contrib-nbextensions --user


"""
**************************************************************************
IPython-contrib-nbextensions - (C) 2013-2016, IPython-contrib Developers - 
All rights reserved.

The IPython-contrib-nbextensions is a permanently updated collection 
of extensions that add functionality to the Jupyter notebook. 
These extensions are mostly written in Javascript and will be loaded 
locally in your Browser. The present program downloads and installs 
the current master of the collection at
https://github.com/ipython-contrib/IPython-notebook-extensions

Installation of the distribution to the current user directories, 
configuration files and paths is done by 
> Jupyter_nb_contribs.py install
Caution: for now, the installation overwrites existing files..

The IPython-contrib repository 
https://github.com/ipython-contrib/IPython-notebook-extensions 
is maintained independently by a group of users and developers and 
not officially related to the IPython development team.

The maturity of the provided extensions may vary, please create 
an issue if you encounter any problems.

Once the extensions are installed, you will be able to look at 
the description of each extension, activate some and play with them 
using the nbextensions server extension by opening a brower tab at 
localhost:8888/nbextensions. Enjoy!

Released under Modified BSD License, read COPYING file for more details.
*************************************************************************
"""


#from distutils.core import setup
from setuptools import setup, find_packages
from os.path import join
from sys import exit, prefix, version_info, argv

#import os, fnmatch
#FILES = [os.path.join(dirpath, f)
#    for dirpath, dirnames, files in os.walk('.')
#    for f in fnmatch.filter(files, '*') if '.git' not in dirpath]



if 'bdist_wheel' in argv:
    raise RuntimeError("This setup.py does not support wheels")

#
#

# pip/setuptools install ------------------------------

classifiers = """\
Development Status :: 1 - Planning
Intended Audience :: End Users/Desktop
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: JavaScript
Programming Language :: Python :: 3
Topic :: Utilities
"""

print(__doc__)

# check python version
ver = (version_info.major, version_info.minor)
if ver < (3, 0):
    print('ERROR: Python 3.x or higher is required.')
    exit(-1)


 
setup(name='Jupyter_contrib_nbextensions_install_utility',
      version='0.0.1',
      description=__doc__.split("\n")[2],
      long_description='\n'.join(__doc__.split("\n")[2:]).strip(),
      author='IPython-contrib Developers',
      author_email='jf.bercher@gmail.com',
      url='https://github.com/ipython-contrib/IPython-notebook-extensions',
      platforms='POSIX',
      keywords=['IPython Jupyter notebook extension'],
      classifiers=filter(None, classifiers.split("\n")),
      license='BSD',
      install_requires = ['ipython >=4','jupyter','psutil','pyaml','requests','clint'],
      scripts = ['Jupyter_notebook_contribs/Jupyter_nb_contribs.py'],
      packages=['Jupyter_notebook_contribs'],
      package_data = {'Jupyter_notebook_contribs': ['*.txt', '*.rst', '*.md']}
      # **addargs
)
