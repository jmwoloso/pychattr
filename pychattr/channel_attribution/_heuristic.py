"""
Contains the model-fitting logic used for the heuristic models.
"""
# Author: Jason Wolosonovich <jason@refinerynet.com>
# License: BSD 3-clause

import functools

import pandas as pd


def _fit_heuristics(df, heuristic, paths, conversions, revenues=None,
                    costs=None, has_rev=False, has_cost=False):
    """Generates the specified heuristic model using partial
    application."""

    def first_touch(d, path_f, conv_f, rev_f=None, cost_f=None,
                    rev=False, cost=False):
        """First-touch attribution model."""
        results = []
        ps = d.loc[:, path_f].values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})

            df_.loc[0, "first_touch_conversions"] = \
                d.loc[i, conv_f].copy()
            df_.loc[1:, "first_touch_conversions"] = 0

            if rev:
                df_.loc[0, "first_touch_revenue"] = \
                    d.loc[i, rev_f].copy()
                df_.loc[1:, "first_touch_revenue"] = 0
            if cost:
                df_.loc[0, "first_touch_cost"] = \
                    d.loc[i, cost_f].copy()
                df_.loc[1:, "first_touch_cost"] = 0

            results.append(df_)

        # combine the results
        df_ = pd.concat(results).reset_index(drop=True)

        agg = {feature: "sum" for feature in df_.columns}.pop("channel")

        # aggregate the results
        return df_.groupby(["channel"], as_index=False).agg(agg)

    def last_touch(d, path_f, conv_f, rev_f=None, cost_f=None,
                   rev=False, cost=False):
        """Last-touch attribution model."""
        results = []
        ps = d.loc[:, path_f].values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})
            idx = len(path) - 1

            df_.loc[idx, "last_touch_conversions"] = \
                d.loc[i, conv_f].copy()
            df_.loc[0: idx - 1, "last_touch_conversions"] = 0

            if rev:
                df_.loc[idx, "last_touch_revenue"] = \
                    d.loc[i, rev_f].copy()
                df_.loc[0: idx - 1, "last_touch_revenue"] = 0
            if cost:
                df_.loc[0, "last_touch_cost"] = \
                    d.loc[i, cost_f].copy()
                df_.loc[0: idx - 1, "last_touch_cost"] = 0

            results.append(df_)

            # combine the results
        df_ = pd.concat(results).reset_index(drop=True)

        agg = {feature: "sum" for feature in df_.columns}.pop("channel")

        # aggregate the results
        return df_.groupby(["channel"], as_index=False).agg(agg)

    def linear_touch(d, path_f, conv_f, rev_f=None, cost_f=None,
                     rev=False, cost=False):
        """Linear touch attribution model."""
        # container to hold the resulting dataframes
        results = []
        ps = d.loc[:, path_f].values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})

            df_.loc[:, "linear_touch_conversions"] = \
                d.loc[i, conv_f].copy() / len(path)

            if rev:
                df_.loc[:, "linear_touch_revenue"] = \
                    d.loc[i, rev_f].copy() / len(path)

            if cost:
                df_.loc[:, "linear_touch_cost"] = \
                    d.loc[i, cost_f].copy() / len(path)

            # append the result for aggregation later on
            results.append(df_)

        # combine the results
        df_ = pd.concat(results).reset_index(drop=True)

        # columns to aggregate
        aggs = {feature: "sum" for feature in df_.columns}.pop(
            "channel")

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    f = functools.partial(eval(heuristic), df, paths, conversions,
                          rev_f=revenues, cost_f=costs, rev=has_rev,
                          cost=has_cost)
    return f


def _ensemble_results(d, heuristics, rev=None, cost=None):
    """Blended version of all the selected heuristic models."""
    df_ = d.copy()

    convs = []
    # these may not be needed
    revs = []
    costs = []

    # get the features we're ensembling
    for heuristic in heuristics:
        convs.append(f"{heuristic}_conversions")
        # these might not be needed
        revs.append(f"{heuristic}_revenue")
        costs.append(f"{heuristic}_cost")

    df_.loc[:, "ensemble_conversions"] = df_.loc[:, convs].copy().sum(
        axis=1)

    if rev:
        df_.loc[:, "ensemble_revenue"] = df_.loc[:, revs].copy().sum(
            axis=1)

    if cost:
        df_.loc[:, "ensemble_cost"] = df_.loc[:, costs].copy().sum(
            axis=1)

    return df_


def fit_heuristic_models(heuristics, df, paths,
                         conversions, revenues=None, costs=None,
                         has_rev=False, has_cost=False):
    """
    Unified interface for fitting the heuristic models.
    """
    results = []
    for heuristic in heuristics:
        if heuristic != "ensemble":
            model = _fit_heuristics(df, heuristic, paths, conversions,
                                    revenues=revenues, costs=costs,
                                    has_rev=has_rev,
                                    has_cost=has_cost)

            # the results of the current model to the results dict
            results.append(model())

    # combine the results
    results = [result.set_index("channel") for result in results]
    results = pd.concat(results, axis=1).reset_index(drop=False)

    # ensemble results
    if "ensemble" in heuristics:
        heuristics.pop(-1)
        results = _ensemble_results(results, heuristics,
                                    rev=has_rev, cost=has_cost)
    return results
