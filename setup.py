#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(name="pychattr",
      version="0.1.0",
      description="Python Channel Attribution",
      author="Jason Wolosonovich",
      author_email="jason@avaland.io",
      url="https://github.com/jmwoloso/pychattr",
      packages=["pychattr"],
      license="GPL-3.0",
      long_description="A Python wrapper around the R "
                       "ChannelAttribution Library",
      install_requires=[
          "Cython==0.28.2",
          "numpy==1.14.5",
          "pandas==0.23.3",
          "rpy2==2.9.4",
          "tzlocal==1.5.1"
      ],
      classifiers=[
          "Development Status :: 0 - Initial",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Topic :: Marketing Channel Attribution",
          "Topic :: Multi-touch Attribution",
          "Operating System :: Unix",
          "Operating System :: MacOS",
          "Operating System :: POSIX",
          "Operating System :: Microsoft :: Windows",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Developers",
          "Intended Audience :: Marketing Operations",
          "Intended Audience :: Data Science",
          "Intended Audience :: Data Analysis"
      ])