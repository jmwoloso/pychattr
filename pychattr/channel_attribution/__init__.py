"""
The Python Channel Attribution (pychattr) package.
"""
# Author: Jason Wolosonovich <jason@refinerynet.com>
# License: BSD 3-clause

from .heuristic import HeuristicModel
from .markov import MarkovModel

__all__ = [
    "HeuristicModel",
    "MarkovModel",
]
