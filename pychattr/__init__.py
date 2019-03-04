"""
Marketing Attribution module for Python
=======================================

pychattr is a Python library providing a variety of canonical
marketing attribution models including Heurisitic (e.g. first-touch,
last-touch, etc.), Markov Chain, Shapley Value and Halo Effect via a
streamlined sklearn-like API.
"""
from .models.channel_attribution import HeuristicModel


#TODO: versioning
__version__ = ""

__author__ = "Jason Wolosonovich, Brett Nebeker, Abhi Sivasailam & " \
             "Ankur Chawla"
__license__ = "BSD 3-Clause"
__maintainer__ = "Jason Wolosonovich, Brett Nebeker, Abhi Sivasailam " \
                 "& Ankur Chawla"
__email__ = "pychattr@avaland.io"

__all__ = [
    "HeuristicModel",
]
