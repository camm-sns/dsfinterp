'''
Created on Jan 15, 2014

@author: Jose Borreguero
'''

from setuptools import setup, find_packages

setup(
  name = 'dsfinterp',
  version = '0.1',

  # Package structure
  #
  # find_packages searches through a set of directories 
  packages = find_packages('dsfinterp', exclude = ['ez_setup','*.tests', '*.tests.*', 'tests.*', 'tests']),
  # package_dir directive maps package names to directories.
  package_dir = {'': 'dsfinterp'},

  # Tests
  #
  # Tests must be wrapped in a unittest test suite by either a
  # function, a TestCase class or method, or a module or package
  # containing TestCase classes. If the named suite is a package,
  # any submodules and subpackages are recursively added to the
  # overall test suite.
  test_suite = 'dsfinterp.tests.suite',

  # Meta information
  author = 'Jose Borreguero',
  author_email = 'borreguero@gmail.com',
  description = 'Cubic Spline Interpolation of Dynamics Structure Factors',
  long_description = open('README.md').read(),
  url = 'https://github.com/camm-sns/dsfinterp',
  download_url = 'http://pypi.python.org/pypi/dsfinterp',
  keywords = ['dynamic structure factor', 'interpolation', 'spline'],
  classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering :: Physics',
  ],
)
