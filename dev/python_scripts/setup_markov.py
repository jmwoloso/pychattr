#!/usr/bin/env python
# TODO: figure out how to 1) test for windows and 2) set the compiler
#  to mingw32 or 64 depending on platform
import sys
if sys.platform == "win32":
    extra_compiler_args="--compiler=mingw32"
else:
    extra_compiler_args=None
try:
    from setuptools import setup
    from setuptools.extension import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from Cython.Distutils import build_ext
from Cython.Build import cythonize

import pychattr

# our cython markov extensions
exts = [
    Extension(
        "markov",
        sources=["markov.pyx", "ChannelAttribution.cpp"],
        language="c++",
        extra_compile_args=extra_compiler_args,
        include_dirs=["src/"]
    )
]

setup(
    name="pychattr",
    version=pychattr.__version__,
    description="Python Channel Attribution",
    author="Jason Wolosonovich",
    author_email="jason@avaland.io",
    url="https://github.com/jmwoloso/pychattr",
    packages=["pychattr"],
    license="GPL-3.0",
    # TODO: update description
    long_description="A Python wrapper around the R "
                     "ChannelAttribution Library",
    # TODO: update requires
    install_requires=[
        "Cython==0.29.4",
        "numpy==1.14.5",
        "pandas==0.23.3",
        "rpy2==2.9.4",
        "tzlocal==1.5.1"
    ],
    # TODO: update classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
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
    ],
    # build our cython extension for the markov model
    ext_modules=cythonize(
        exts,
        compiler_directives={
            "language_level": "3"
        }
    ),
    cmdclass={
        "build_ext": build_ext
    }
)
