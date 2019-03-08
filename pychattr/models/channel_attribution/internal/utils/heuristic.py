"""
heuristic.py: Various utility functions used during construction of
the heuristic models.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause

import pandas as pd

from ..logic.heuristic import fit_heuristics


def ensemble_results(paths, conversions, revenues, costs, separator):
    """Blended version of all the selected heuristic models."""
    raise NotImplementedError("This model specification will be "
                              "available in the next minor "
                              "release of pychattr.")


def fit_heuristic_models(heuristics, df, paths, conversions, sep,
                         revenues=None, costs=None,
                         lead_channel=None, oppty_channel=None,
                         decay_rate=7, path_dates=None,
                         conv_dates=None):
    """
    Fits the specified heuristic models.
    """
    results_ = []
    for heuristic in heuristics:
        if heuristic != "ensemble_model":
            model = fit_heuristics(df, heuristic, paths, conversions,
                                   sep, revenues=revenues, costs=costs,
                                   lead_channel=lead_channel,
                                   oppty_channel=oppty_channel,
                                   decay_rate=decay_rate,
                                   path_dates=path_dates,
                                   conv_dates=conv_dates)

            # the results of the current model to the results dict
            results_.append(model())
            # combine the results and return
            return pd.concat(results_, axis=1)
        # not implemented yet
        else:
            # use pd.merge(l,r, on="channel") then average across the
            # row making a new column called ensemble
            raise NotImplementedError(
                "This model specification will be "
                "available in the next minor "
                "release of pychattr.")
