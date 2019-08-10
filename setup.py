#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import pychattr

setup(name="pychattr",
      version=pychattr.__version__,
      description="Python Channel Attribution",
      author="Jason Wolosonovich",
      author_email="jason@refinerynet.com",
      url="https://github.com/jmwoloso/pychattr",
      packages=find_packages(include=["pychattr", "pychattr.*"]),
      license="BSD 3-clause",
      long_description="Marketing Attribution for Python",
      install_requires=[
          "numpy",
          "pandas"
      ],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries :: Python "
          "Modules",
          "Topic :: Scientific/Engineering",
          "Operating System :: Unix",
          "Operating System :: MacOS",
          "Operating System :: POSIX",
          "Operating System :: Microsoft :: Windows",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Other Audience",
          "Intended Audience :: Information Technology"
      ])
