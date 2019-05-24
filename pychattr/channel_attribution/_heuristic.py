"""
Contains the model-fitting logic used for the heuristic models.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause

import functools

import numpy as np
import pandas as pd


def _fit_heuristics(df, heuristic, paths, conversions, sep,
                    revenues=None, costs=None, lead_channel=None,
                    oppty_channel=None, decay_rate=7, path_dates=None,
                    conv_dates=None, has_rev=False, has_cost=False):
    """Generates the specified heuristic model using partial
    application."""
    # TODO: put in checks for each that paths meet the minimum
    #  requirements for the specific heuristic function (e.g.
    #  z-shaped needs at least 5 channels per path in order to apply
    #  weights correctly)

    def first_touch(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                    rev=False, cost=False):
        """First-touch attribution model."""
        results = []
        ps = d.loc[:, path_f].values
        # ps = d.loc[:, path_f].apply(
        #     lambda s: s.split(sp)
        # ).values

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

    def last_touch(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                   rev=False, cost=False):
        """Last-touch attribution model."""
        results = []
        ps = d.loc[:, path_f].values
        # ps = d.loc[:, path_f].apply(
        #     lambda s: s.split(sp)
        # ).values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})
            idx = len(path) - 1

            df_.loc[idx, "last_touch_conversions"] = \
                d.loc[i, conv_f].copy()
            df_.loc[0: idx-1, "last_touch_conversions"] = 0

            if rev:
                df_.loc[idx, "last_touch_revenue"] = \
                    d.loc[i, rev_f].copy()
                df_.loc[0: idx-1, "last_touch_revenue"] = 0
            if cost:
                df_.loc[0, "last_touch_cost"] = \
                    d.loc[i, cost_f].copy()
                df_.loc[0: idx-1, "last_touch_cost"] = 0

            results.append(df_)

            # combine the results
        df_ = pd.concat(results).reset_index(drop=True)

        agg = {feature: "sum" for feature in df_.columns}.pop("channel")

        # aggregate the results
        return df_.groupby(["channel"], as_index=False).agg(agg)

    def linear_touch(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                     rev=False, cost=False):
        """Linear touch attribution model."""
        # container to hold the resulting dataframes
        results = []
        ps = d.loc[:, path_f].values
        # ps = d.loc[:, path_f].apply(lambda s: s.split(sp)).values

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

    def u_shaped(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                 rev=False, cost=False):
        """U-shaped (position-based) attribution model."""
        # container to hold the resulting dataframes
        results = []
        ps = d.loc[:, path_f].values
        # ps = d.loc[:, path_f].apply(lambda s: s.split(sp)).values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})

            # we really need at least 3 channels for this model type
            if len(path) < 3:
                # this just becomes a linear model
                df_.loc[:, "u_shaped_conversions"] = \
                    d.loc[i, conv_f].copy() / len(path)

                if rev:
                    df_.loc[:, "u_shaped_revenue"] = \
                        d.loc[i, rev_f].copy() / len(path)

                if cost:
                    df_.loc[:, "u_shaped_cost"] = \
                        d.loc[i, cost_f].copy() / len(path)
            else:
                ix = list(range(len(path)))
                idx = [0, len(path) - 1]

                ix.pop(idx[0])
                ix.pop(-1)

                df_.loc[idx, "u_shaped_conversions"] = \
                    0.4 * d.loc[i, conv_f].copy()

                df_.loc[ix, "u_shaped_conversions"] = \
                    (0.2 / len(ix)) * d.loc[i, conv_f].copy()

                if rev:
                    df_.loc[idx, "u_shaped_revenue"] = \
                        0.4 * d.loc[i, rev_f].copy()

                    df_.loc[ix, "u_shaped_revenue"] = \
                        (0.2 / len(ix)) * d.loc[i, rev_f].copy()

                if cost:
                    df_.loc[idx, "u_shaped_cost"] = \
                        0.4 * d.loc[i, cost_f]

                    df_.loc[ix, "u_shaped_cost"] = \
                        (0.2 / len(ix)) * d.loc[i, cost_f].copy()

            # append the result for aggregation later on
            results.append(df_)

            # combine the results
        df_ = pd.concat(results).reset_index(drop=True)

        # columns to aggregate
        aggs = {feature: "sum" for feature in df_.columns}.pop(
            "channel")

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def w_shaped(d, path_f, conv_f, sp, lead_channel, rev_f=None,
                 cost_f=None, rev=False, cost=False):
        """W-shaped attribution model."""
        # container to hold the resulting dataframes
        results = []
        ps = d.loc[:, path_f].values
        # ps = d.loc[:, path_f].apply(lambda s: s.split(sp)).values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})

            # we really need at least 4 channels for this model type
            if len(path) < 4:
                # this just becomes a linear model
                df_.loc[:, "w_shaped_conversions"] = \
                    d.loc[i, conv_f].copy() / len(path)

                if rev:
                    df_.loc[:, "w_shaped_revenue"] = \
                        d.loc[i, rev_f].copy() / len(path)

                if cost:
                    df_.loc[:, "w_shaped_cost"] = \
                        d.loc[i, cost_f].copy() / len(path)
            else:
                # get all indices in the current path
                ix = list(range(len(path)))

                # indices of the major channels
                idx = [0, np.argmax(np.array(path) == lead_channel),
                       len(path) - 1]

                # remove indices of major channels
                ix.pop(idx[1])
                ix.pop(0)
                ix.pop(-1)

                # apply the weight to the major channels
                df_.loc[idx, "w_shaped_conversions"] = \
                    0.3 * d.loc[i, conv_f].copy()

                # apply the weight to the minor channels
                df_.loc[ix, "w_shaped_conversions"] = \
                    (0.1 / len(ix)) * d.loc[i, conv_f].copy()

                if rev:
                    df_.loc[idx, "w_shaped_revenue"] = \
                        0.3 * d.loc[i, rev_f].copy()

                    df_.loc[ix, "w_shaped_revenue"] = \
                        (0.1 / len(ix)) * d.loc[i, rev_f].copy()

                if cost:
                    df_.loc[idx, "w_shaped_cost"] = \
                        0.3 * d.loc[i, cost_f].copy()

                    df_.loc[ix, "w_shaped_cost"] = \
                        (0.1 / len(ix)) * d.loc[i, cost_f].copy()

            # append the result for aggregation later on
            results.append(df_)

        # combine the results
        df_ = pd.concat(results)

        # columns to aggregate
        aggs = {feature: "sum" for feature in df_.columns}.pop(
            "channel")

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def z_shaped(d, path_f, conv_f, sp, lead_channel, oppty_channel,
                 rev_f=None, cost_f=None, rev=False, cost=False):
        """Z-shaped (full path) attribution model."""
        # container to hold the resulting dataframes
        results = []
        ps = d.loc[:, path_f].values
        # ps = d.loc[:, path_f].apply(lambda s: s.split(sp)).values

        for i, path in enumerate(ps):
            df_ = pd.DataFrame({"channel": path})

            # we really need at least 5 channels for this model type
            if len(path) < 5:
                # this just becomes a linear model
                df_.loc[:, "z_shaped_conversions"] = \
                    d.loc[i, conv_f].copy() / len(path)

                if rev:
                    df_.loc[:, "z_shaped_revenue"] = \
                        d.loc[i, rev_f].copy() / len(path)

                if cost:
                    df_.loc[:, "z_shaped_cost"] = \
                        d.loc[i, cost_f].copy() / len(path)
            else:
                # get all indices in the current path
                ix = list(range(len(path)))

                # indices of the major channels
                idx = [
                    0,
                    np.argmax(np.array(path) == lead_channel),
                    np.argmax(np.array(path) == oppty_channel),
                    len(path) - 1
                ]

                # remove indices of major channels
                ix.pop(idx[1])
                ix.pop(idx[2] - 1)
                ix.pop(0)
                ix.pop(-1)

                # apply the weight to the major channels
                df_.loc[idx, "z_shaped_conversions"] = \
                    0.225 * d.loc[i, conv_f].copy()

                # apply the weight to the minor channels
                df_.loc[ix, "z_shaped_conversions"] = \
                    (0.1 / len(ix)) * d.loc[i, conv_f].copy()

                if rev:
                    df_.loc[idx, "z_shaped_revenue"] = \
                        0.225 * d.loc[i, rev_f].copy()

                    df_.loc[ix, "z_shaped_revenue"] = \
                        (0.1 / len(ix)) * d.loc[i, rev_f].copy()

                if cost:
                    df_.loc[idx, "z_shaped_cost"] = \
                        0.225 * d.loc[i, cost_f].copy()

                    df_.loc[ix, "z_shaped_cost"] = \
                        (0.1 / len(ix)) * d.loc[i, cost_f].copy()

            # append the result for aggregation later on
            results.append(df_)

        # combine the results
        df_ = pd.concat(results)

        # columns to aggregate
        aggs = {feature: "sum" for feature in df_.columns}.pop(
            "channel")

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def time_decay(d, path_f, conv_f, sp, path_dates, conv_dates,
                   dr=7, rev_f=None, cost_f=None, rev=False,
                   cost=False):
            """Time decay attribution model."""

            def get_weight(days_to_conversion, decay_rate):
                """Takes the days-to-conversion and calculates the
                attribution weight using the decay rate supplied."""
                return np.exp2(-days_to_conversion / decay_rate)

            get_weight_v = np.vectorize(get_weight)

            # container to hold the resulting dataframes
            results = []
            ps = d.loc[:, path_f].values
            # ps = d.loc[:, path_f].apply(lambda s: s.split(sp))\
            #     .values
            dates = d.loc[:, path_dates].apply(lambda s: s.split(
                sp)).values
            c_dates = d.loc[:, conv_dates].values

            # iterate through the paths and calculate the linear touch
            # model
            for i, (path, date, c_date) in enumerate(zip(ps, dates,
                                                         c_dates)):
                df_ = pd.DataFrame(
                    {
                        "channel": path,
                        "channel_date": date,
                        "conv_date": [c_date] * len(path)
                    }
                )

                # get the days before conversion for each channel in
                # the current path
                df_.loc[:, "dbc"] = (
                    df_.loc[:, "conv_date"]
                    .astype("datetime64[ns]").copy() -
                    df_.loc[:, "channel_date"]
                    .astype("datetime64[ns]").copy()
                ) / np.timedelta64(1, "D")

                df_.loc[:, "weight"] = \
                    get_weight_v(df_.loc[:, "dbc"], dr)

                # adjust weights proportionally
                df_.loc[:, "weight"] /= df_.loc[:, "weight"].sum()

                df_.loc[:, "time_decay_conversions"] = \
                    df_.loc[:, "weight"] * d.loc[i, conv_f].copy()

                if rev:
                    df_.loc[:, "time_decay_revenue"] = \
                        df_.loc[:, "weight"] * d.loc[i, rev_f].copy()
                if cost:
                    df_.loc[:, "time_decay_cost"] = \
                        df_.loc[:, "weight"] * d.loc[i, cost_f].copy()

                df_ = df_.drop(columns=["dbc", "weight"])

                # append the result for aggregation later on
                results.append(df_)

            # combine the results
            df_ = pd.concat(results)

            # columns to aggregate
            aggs = {feature: "sum" for feature in df_.columns}.pop(
                "channel")

            return df_.groupby(["channel"], as_index=False).agg(aggs)

    # TODO: is there a cleaner way to do this?
    # the explicitly-named models need extra parameters sent to them
    if heuristic == "w_shaped":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, lead_channel, rev_f=revenues,
                              cost_f=costs, rev=has_rev, cost=has_cost)

    elif heuristic == "z_shaped":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, lead_channel, oppty_channel,
                              rev_f=revenues, cost_f=costs, rev=has_rev,
                              cost=has_cost)

    elif heuristic == "time_decay":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, path_dates, conv_dates,
                              dr=decay_rate, rev_f=revenues,
                              cost_f=costs, rev=has_rev, cost=has_cost)

    else:
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, rev_f=revenues, cost_f=costs,
                              rev=has_rev, cost=has_cost)
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
                         conversions, sep, revenues=None, costs=None,
                         lead_channel=None, oppty_channel=None,
                         decay_rate=7, path_dates=None,
                         conv_dates=None, has_rev=False,
                         has_cost=False):
    """
    Unified interface for fitting the heuristic models.
    """
    results = []
    for heuristic in heuristics:
        if heuristic != "ensemble":
            model = _fit_heuristics(df, heuristic, paths, conversions,
                                    sep, revenues=revenues, costs=costs,
                                    lead_channel=lead_channel,
                                    oppty_channel=oppty_channel,
                                    decay_rate=decay_rate,
                                    path_dates=path_dates,
                                    conv_dates=conv_dates,
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
