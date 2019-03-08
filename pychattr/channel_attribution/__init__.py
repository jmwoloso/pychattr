"""
The pychattr Channel Attribution package.
"""
# Author: Jason Wolosonovich
# License: BSD 3-clause

from .heuristic import HeuristicModel
from .markov import MarkovModel

__all__ = [
    "HeuristicModel",
    "MarkovModel",
]
