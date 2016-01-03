#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
*******************************************************************************
IPython-contrib-nbextensions - (C) 2013-2016, IPython-contrib Developers - 
All rights reserved.

This installs a collection of extensions that add functionality to the Jupyter 
notebook. These extensions are mostly written in Javascript and will be loaded 
locally in your Browser. 

The IPython-contrib repository 
https://github.com/ipython-contrib/IPython-notebook-extensions 
is maintained independently by a group of users and developers and not 
officially related to the IPython development team.

The maturity of the provided extensions may vary, please create an issue if 
you encounter any problems.

Once the extensions are installed, you will be able to look at the description
of each extension, activate some and play with them using the nbextensions 
server extension by opening a brower tab at localhost:8888/nbextensions. Enjoy!

Released under Modified BSD License, read COPYING file for more details.
*******************************************************************************
"""


#from distutils.core import setup
from setuptools import setup, find_packages
from setuptools.command.install import install
from sys import exit, prefix, version_info, argv

def downloadWithPprogressbar(file_url,path):
	import requests
	from clint.textui import progress

	r = requests.get(file_url, stream=True)
	with open(path, 'wb') as f:
		total_length = int(r.headers.get('content-length'))
		for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
			if chunk:
				f.write(chunk)
				f.flush()

def downloadDistrib():
	import os
	filename = "https://github.com/ipython-contrib/IPython-notebook-extensions/archive/master.zip"

	# make a temp dir
	import tempfile
	p=tempfile.mkdtemp()
	p='.'

	# Download and uncompress
	#import pip
	#pip.main(['install','--download='+p, '--no-deps' ,filename])
	downloadWithPprogressbar(filename,os.path.join(p,"master.zip"))
	
	import zipfile
	z=zipfile.ZipFile(os.path.join(p,"master.zip"))
	z.extractall(p)
	#pip.utils.unzip_file(os.path.join(p,"master.zip"),p)
	return os.path.join(p,"IPython-notebook-extensions-master")

def recursive_copy(src, dest, update=0, verbose=0):
    import distutils
    distutils.dir_util.copy_tree(src, dest, update=update, verbose=verbose)

def installNbExtensions(p, update=0,verbose=0, debug = False):
	
	# Install notebook extensions

	from jupyter_core.paths import jupyter_data_dir
	import os
	import sys
	import shutil
	import IPython
	import notebook

	if IPython.__version__[0] < '4':
	    print("IPython version 4.x is required")
	    exit(1)

	print("Installing Jupyter notebook extensions.")

	
	#
	# 1. Get the local configuration file path
	#
	data_dir = os.getenv('PREFIX', None)
	if data_dir == None:
	    data_dir = jupyter_data_dir()
	else:
	    data_dir = os.path.join(data_dir, 'share/jupyter')

	print("Extensions and templates path: %s" % data_dir)

	if os.path.exists(data_dir) is False:
	    os.mkdir(data_dir)
	    if debug is True: print("Creating directory %s" % data_dir)

	#
	# 2. Install files
	#
		
	# copy extensions to IPython extensions directory
	src = os.path.join(p,'extensions')
	destination = os.path.join(data_dir, 'extensions')
	if debug is True: print("Install Python extensions to %s" % destination)
	recursive_copy(src, destination,update=update)

	# Install templates
	src = os.path.join(p,'templates')
	destination = os.path.join(data_dir, 'templates')
	if debug is True: print("Install templates to %s" % destination)
	recursive_copy(src, destination,update=update)

	# Install nbextensions
	src = os.path.join(p,'nbextensions')
	destination = os.path.join(data_dir, 'nbextensions')
	if debug is True: print("Install notebook extensions to %s" % destination)
	recursive_copy(src, destination,update=update)


def configureNbExtensions():
	#import Jupyter_notebook_contribs
	from Jupyter_notebook_contribs import configure_nbextensions


class InstallNbExt(install):
	def run(self):
		import pip, os, Jupyter_notebook_contribs
		filepath = os.path.abspath(os.path.dirname(Jupyter_notebook_contribs.__file__))
		reqfile=os.path.join(filepath,"requirements.txt")
		print("Installing requirements (should have already been installed)")
		pip.main(["install","-r", reqfile,'--user'])

		print("Installing the nbextensions")
		p = downloadDistrib()
		installNbExtensions(p,update=0,verbose=0)
		configureNbExtensions()

class UpdateNbExt(install):
	def run(self):
		print("Updating the nbextensions")
		p = downloadDistrib()
		installNbExtensions(p,update=1,verbose=1)
# Unfortunately, for now, the installation overwrites existing files..
# This is because the timestamps in the zip file are the timestamps of the last, current master, at the date of the very last update..

class ConfigureNbExt(install):
	def run(self):
		print("Reconfiguring the nbextensions")
		configureNbExtensions()



# pip/setuptools install ------------------------------

def main(*args):

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



	setup(name='Python-contrib-nbextensions',
	      version='0.0.1',
	      description=__doc__.split("\n")[2],
	      long_description='\n'.join(__doc__.split("\n")[2:]).strip(),
	      author='IPython-contrib Developers',
	      author_email='@gmail.com',
	      url='https://github.com/ipython-contrib/IPython-notebook-extensions',
	      platforms='POSIX',
	      keywords=['IPython Jupyter notebook extension'],
	      classifiers=filter(None, classifiers.split("\n")),
	      license='BSD',
	      install_requires = ['ipython >=4','jupyter','psutil','pyaml','zozo'],
	      cmdclass={
		'install' : InstallNbExt,
		'update' : UpdateNbExt,
		'reconfigure':  ConfigureNbExt,
		},
	      #packages=['IPython-contrib-nbextensions'],
	      # **addargs
	)

if __name__ == '__main__':	
    import argparse
    print(main.__doc__)
    whatitdoes="""This program downloads the current master of the collection\n
           of Ipython-contrib noteboook extensions. \n
	   https://github.com/ipython-contrib/IPython-notebook-extensions\n
           Then it may be used to install the distribution to the current\n 
           user directories, reconfigure the configuration files and paths. \n
           Caution: for now, the installation overwrites existing files.."""
    myself="(c) IPython-contrib developers"
    parser = argparse.ArgumentParser(description=whatitdoes, epilog=myself)
    # mandatory argument
    parser.add_argument('command', choices=['install',  'reconfigure'],
    help = r'',
    default = 'install', type = str,  nargs = 1)
    arguments = parser.parse_args()
    main(arguments.command[0])


