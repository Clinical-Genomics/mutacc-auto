#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree
import subprocess

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'mutacc_auto'
DESCRIPTION = ''
URL = 'https://github.com/Clinical-Genomics/mutacc-auto.git'
EMAIL = 'adam.rosenbaum@scilifelab.se'
AUTHOR = 'Adam Rosenbaum'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

#Required versions of mutacc
SCOUT_VERSION = '4.2.2'
HOUSEKEEPER_VERSION = '2.2.8'
MUTACC_VERSION = '1.0.0'

here = os.path.abspath(os.path.dirname(__file__))

def parse_reqs(req_path='./requirements.txt'):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with io.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle
                 if line.strip() and not line.startswith('#'))

        for line in lines:
            # check for nested requirements files
            if line.startswith('-r'):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])

            else:
                # add the line as a new requirement
                install_requires.append(line)

    return install_requires

# What packages are required for this module to be executed?
REQUIRED = parse_reqs()

### Check if Scout and HouseKeeper are installed

def check_scout():

    try:
        scout_output = subprocess.check_output(['scout', '--version']).decode('utf-8')

    except OSError as error:
        sys.exit('scout does not exist')

    scout_version = int(scout_output.split(' ')[-1].replace('.', ''))
    min_scout_version = int(SCOUT_VERSION.replace('.',''))

    if scout_version >= min_scout_version:

        return True

def check_housekeeper():

    try:
        hk_output = subprocess.check_output(['housekeeper', '--version']).decode('utf-8')

    except OSError as error:
        sys.exit('housekeeper does not exist')

    hk_version = int(hk_output.split(' ')[-1].replace('.', ''))
    min_hk_version = int(HOUSEKEEPER_VERSION.replace('.',''))

    if hk_version >= min_hk_version:

        return True

def check_mutacc():

    try:
        mutacc_output = subprocess.check_output(['mutacc', '--version']).decode('utf-8')

    except OSError as error:
        sys.exit('mutacc does not exist')

    mutacc_version = int(mutacc_output.split(' ')[-1].replace('.', ''))
    min_mutacc_version = int(MUTACC_VERSION.replace('.',''))

    if mutacc_version >= min_mutacc_version:

        return True

#Check if istallation is made on Travis CI
istravis = os.environ.get('TRAVIS') == 'true'
if not istravis:
    #if not check_scout(): sys.exit('Dependency problem: scout >= {} is required'.format(SCOUT_VERSION))
    #if not check_housekeeper(): sys.exit('Dependency problem: housekeeper >= {} is required'.format(HOUSEKEEPER_VERSION))
    if not check_mutacc(): sys.exit('Dependency problem: mutacc >= {} is required'.format(MUTACC_VERSION))
###

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests/','scripts/')),
    entry_points={
        'console_scripts': ['mutacc-auto=mutacc_auto.cli.root:cli'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
