"""
heuristic.py: Various utility functions used during construction of
the heuristic models.
"""
import pandas as pd

from ..logic.heuristic import fit_model


def fit_heuristic_models(heuristics, df, paths, conversions, sep,
                         revenues=None, costs=None,
                         exclude_direct=False, direct_channel=None,
                         lead_channel=None, oppty_channel=None,
                         decay_rate=7, path_dates=None,
                         conv_dates=None):
    """
    Fits the specified heuristic models.
    """
    results_ = []
    for heuristic in heuristics:
        if heuristic != "ensemble_model":
            model = fit_model(df, heuristic, paths, conversions, sep,
                              revenues=revenues, costs=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel,
                              lead_channel=lead_channel,
                              oppty_channel=oppty_channel,
                              decay_rate=decay_rate, path_dates=path_dates,
                              conv_dates=conv_dates)

            # the results of the current model to the results dict
            results_.append(model)
            # combine the results and return
            return pd.concat(results_, axis=1)
        # not implemented yet
        else:
            raise NotImplementedError(
                "This model specification will be "
                "available in the next minor "
                "release of pychattr.")
