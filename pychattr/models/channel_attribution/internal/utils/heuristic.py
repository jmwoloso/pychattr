"""
heuristic.py: Various utility functions used during construction of
the heuristic models.
"""
import pandas as pd
from ..logic.heuristic import fit_model


def fit_heuristic_models(heuristics, df, paths, conversions,
                         revenues, costs, separator):
    """
    Fits the specified heuristic models.
    """
    results = []
    for heuristic in heuristics:
        if heuristic == "ensemble_model":
            # TODO: might want to break this out of the partial
            #  application function (fit_model)
            model = fit_model(df, paths, conversions, revenues, costs,
                              separator, heuristic=heuristic)

        model = fit_model(df, paths, conversions, revenues, costs,
                          separator, heuristic=heuristic)

        # the results of the current model to the results dict
        results.append(model)

    # combine the results and return
    return pd.concat(results)
