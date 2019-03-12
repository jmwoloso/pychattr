"""
Contains the model-fitting logic used for the Markov model.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause
import itertools

import numpy as np


def _get_transition_matrix(transitions, unique_channels):
    """
    Creates the transition matrix from the supplied transitions
    and set of unique channels.

    Adapted from: https://gist.github.com/tg12/d7efa579ceee4afbeaec97eb442a6b72
    """
    # n x n matrix
    n = len(unique_channels)

    M = [[0] * n for _ in range(n)]

    for transition in transitions:
        for (i,j) in zip(transition, transition[1:]):
            M[i][j] += 1

    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [f / s for f in row]

    return np.asarray(M)


def _get_markov_components(df, path_f):
    """Calculate the transition probability matrix for the given
    paths."""
    # get the paths
    paths = df.loc[:, path_f].values

    # container for the channels
    channels = []

    # iterate through the paths and append the channels
    for path in paths:
        for channel in path:
            channels.append(channel)

    # get a list of unique channels
    unique_channels = np.unique(channels)

    # map channel -> int for calculating the transition matrix
    channel_mapper = {channel: i for i, channel in enumerate(
        unique_channels)}

    # unmap int -> channel
    channel_unmapper = {v: k for k, v in channel_mapper.items()}

    # container for the mapped paths
    mapped_paths = []

    # iterate through the paths and map them to ints
    for i, path in enumerate(paths):
        mapped_channels = []
        for channel in path:
            mapped_channels.append(channel_mapper[channel])
        mapped_paths.append(mapped_channels)

    # calculate the transition matrix
    trans_mat = _get_transition_matrix(mapped_paths, unique_channels)

    return trans_mat, channel_mapper, channel_unmapper


def markov_memory(iterable, k_order):
    """
    Returns the ordered k_order tuples and number of occurrences of each
    for the specified path.

    Adapted from an itertools recipe.
    """
    a, b = itertools.tee(iterable)
    ordered_pairs = list(zip(a, itertools.islice(b, 1, None)))
    # d = dict(collections.Counter(ordered_pairs))
    # e = collections.defaultdict(dict)
    #
    # for (c1, c2) in ordered_pairs:
    #     e[c1] = collections.defaultdict(int)
    #     e[c1][c2] += d[(c1, c2)]

    # return d
    return ordered_pairs


def fit_markov(df, paths, conversions, sep, revenues=None, costs=None):
    """Markov attribution model."""
    trans_mat, channel_mapper, channel_unmapper = \
        _get_markov_components(df, paths)

    return trans_mat, channel_mapper, channel_unmapper
