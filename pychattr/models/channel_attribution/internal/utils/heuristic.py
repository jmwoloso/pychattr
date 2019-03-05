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
                         half_life=7, path_dates=None, conv_dates=None):
    """
    Fits the specified heuristic models.
    """
    results = []
    for heuristic in heuristics:
        if heuristic == "ensemble_model":
            # TODO: might want to break this out of the partial
            #  application function (fit_model)
            model = fit_model(df, heuristic, paths, conversions, sep,
                              revenues=revenues, costs=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel,
                              lead_channel=lead_channel,
                              oppty_channel=oppty_channel,
                              half_life=half_life,
                              path_dates=path_dates,
                              conv_dates=conv_dates)

        model = fit_model(df, heuristic, paths, conversions, sep,
                          revenues=revenues, costs=costs,
                          exclude_direct=exclude_direct,
                          direct_channel=direct_channel,
                          lead_channel=lead_channel,
                          oppty_channel=oppty_channel,
                          half_life=half_life, path_dates=path_dates,
                          conv_dates=conv_dates, )

        # the results of the current model to the results dict
        results.append(model)

    # combine the results and return
    return pd.concat(results)
