from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

setup(
    name="pychattr",
    version="0.1.dev0",
    packages=["pychattr",],
    license="GPLv3",
    long_description=open("README.txt").read(),
    ext_modules=[Extension("pychattr",
                           ["channel_attribution_wrapper.pyx"],
                           library_dirs=os.getcwd() + "/src/")],
    setup_requires=["pandas"]
)