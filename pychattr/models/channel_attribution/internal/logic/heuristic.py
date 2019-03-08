"""
Contains the model fitting logic used for the heuristic models.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause

import functools

import numpy as np
import pandas as pd


def fit_heuristics(df, heuristic, paths, conversions, sep,
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
        df_ = pd.DataFrame(columns=["channel"])

        df_.loc[:, "channel"] = d.loc[:, path_f].apply(
            lambda s: s.split(sp)[0]
        )

        # give the first channels in each path all the credit
        df_.loc[:, "first_touch_conversions"] = d.loc[:, conv_f].copy()

        if rev:
            df_.loc[:, "first_touch_revenue"] = d.loc[:, rev_f].copy()

        if cost:
            df_.loc[:, "first_touch_cost"] = d.loc[:, cost_f].copy()

        agg = {feature: "sum" for feature in df_.columns}.pop("channel")

        # aggregate the results
        return df_.groupby(["channel"], as_index=False).agg(agg)

    def last_touch(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                   rev=False, cost=False):
        """Last-touch attribution model."""
        df_ = pd.DataFrame(columns=["channel"])

        df_.loc[:, "channel"] = d.loc[:, path_f].apply(
            lambda s: s.split(sp)[-1]
        )

        # give the last channels in each path all the credit
        df_.loc[:, "last_touch_conversions"] = d.loc[:, conv_f].copy()
        if rev:
            df_.loc[:, "last_touch_revenue"] = d.loc[:, rev_f].copy()
        if cost:
            df_.loc[:, "last_touch_cost"] = d.loc[:, cost_f].copy()

        agg = {feature: "sum" for feature in df_.columns}.pop("channel")

        # aggregate the results
        return df_.groupby(["channel"], as_index=False).agg(agg)

    def linear_touch(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                     rev=False, cost=False):
        """Linear touch attribution model."""
        # container to hold the resulting dataframes
        results = []

        paths = d.loc[:, path_f].apply(lambda s: s.split(sp))

        # iterate through the paths and calculate the linear touch model
        for i, path in enumerate(paths):
            features = [
                "channel",
                "linear_touch_conversions"
            ]

            if rev:
                features.append("linear_touch_revenue")
            if cost:
                features.append("linear_touch_cost")

            # dataframe to hold the results of this iteration
            df_ = pd.DataFrame(columns=features)

            # add the channels to the dataframe
            for j, channel in enumerate(path):
                df_.loc[j, "channel"] = channel

            # divide the values evenly among the channels
            weight = 1 / df_.shape[0]

            # apply the weights to the values
            df_.loc[:, "linear_touch_conversions"] = \
                d.loc[i, conv_f].copy() * weight

            if rev:
                df_.loc[:, "linear_touch_revenue"] = \
                    d.loc[i, rev_f].copy() * weight
            if cost:
                df_.loc[:, "linear_touch_cost"] = \
                    d.loc[i, cost_f].copy() * weight

            # append the result for aggregation later on
            results.append(df_)

        # combine the results
        df_ = pd.concat(results)

        # columns to aggregate
        aggs = {feature: "sum" for feature in df_.columns}.pop(
            "channel")

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def u_shaped(d, path_f, conv_f, sp, rev_f=None, cost_f=None,
                 rev=False, cost=False):
        """U-shaped (position-based) attribution model."""
        # container to hold the resulting dataframes
        results = []

        paths = d.loc[:, path_f].apply(lambda s: s.split(sp))

        # iterate through the paths and calculate the linear touch model
        for i, path in enumerate(paths):
            features = [
                "channel",
                "u_shaped_conversions"
            ]

            if rev:
                features.append("u_shaped_revenue")
            if cost:
                features.append("u_shaped_cost")

            # dataframe to hold the results of this iteration
            df_ = pd.DataFrame(columns=features)

            # for clarity
            first_channel = path[0]
            last_channel = path[-1]

            # add the channels to the dataframe
            for j, channel in enumerate(path):
                df_.loc[j, "channel"] = channel
                if channel in [first_channel, last_channel]:
                    df_.loc[j, "weight"] = 0.4
                else:
                    df_.loc[j, "weight"] = 0.2 / (len(paths[i]) - 2)

            # apply the weights to the values
            df_.loc[:, "u_shaped_conversions"] = \
                d.loc[i, conv_f].copy() * df_.loc[:, "weight"]

            if rev:
                df_.loc[:, "u_shaped_revenue"] = \
                    d.loc[i, rev_f].copy() * df_.loc[:, "weight"]
            if cost:
                df_.loc[:, "u_shaped_cost"] = \
                    d.loc[i, cost_f].copy() * df_.loc[:, "weight"]

            df_ = df_.drop(columns=["weight"])

            # append the result for aggregation later on
            results.append(df_)

        # combine the results
        df_ = pd.concat(results)

        # columns to aggregate
        aggs = {feature: "sum" for feature in df_.columns}.pop(
            "channel")

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def w_shaped(d, path_f, conv_f, sp, lead_channel, rev_f=None,
                 cost_f=None, rev=False, cost=False):
        """W-shaped attribution model."""
        # container to hold the resulting dataframes
        results = []

        paths = d.loc[:, path_f].apply(lambda s: s.split(sp))

        # iterate through the paths and calculate the linear touch model
        for i, path in enumerate(paths):
            features = [
                "channel",
                "w_shaped_conversions"
            ]

            if rev:
                features.append("w_shaped_revenue")
            if cost:
                features.append("w_shaped_cost")

            # dataframe to hold the results of this iteration
            df_ = pd.DataFrame(columns=features)

            # for clarity
            first_channel = path[0]
            last_channel = path[-1]

            # add the channels to the dataframe
            for j, channel in enumerate(path):
                df_.loc[j, "channel"] = channel
                if channel in [first_channel, lead_channel,
                               last_channel]:
                    df_.loc[j, "weight"] = 0.3
                else:
                    df_.loc[j, "weight"] = 0.1 / (len(paths[i]) - 3)

            # apply the weights to the values
            df_.loc[:, "w_shaped_conversions"] = \
                d.loc[i, conv_f].copy() * df_.loc[:, "weight"]

            if rev:
                df_.loc[:, "w_shaped_revenue"] = \
                    d.loc[i, rev_f].copy() * df_.loc[:, "weight"]
            if cost:
                df_.loc[:, "w_shaped_cost"] = \
                    d.loc[i, cost_f].copy() * df_.loc[:, "weight"]

            df_ = df_.drop(columns=["weight"])

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

        paths = d.loc[:, path_f].apply(lambda s: s.split(sp))

        # iterate through the paths and calculate the linear touch model
        for i, path in enumerate(paths):
            features = [
                "channel",
                "z_shaped_conversions"
            ]

            if rev:
                features.append("z_shaped_revenue")
            if cost:
                features.append("z_shaped_cost")

            # dataframe to hold the results of this iteration
            df_ = pd.DataFrame(columns=features)

            # for clarity
            first_channel = path[0]
            last_channel = path[-1]

            # add the channels to the dataframe
            for j, channel in enumerate(path):
                df_.loc[j, "channel"] = channel
                if channel in [first_channel, lead_channel,
                               oppty_channel, last_channel]:
                    df_.loc[j, "weight"] = 0.225
                else:
                    df_.loc[j, "weight"] = 0.1 / (len(paths[i]) - 3)

            # apply the weights to the values
            df_.loc[:, "z_shaped_conversions"] = \
                d.loc[i, conv_f].copy() * df_.loc[:, "weight"]

            if rev:
                df_.loc[:, "z_shaped_revenue"] = \
                    d.loc[i, rev_f].copy() * df_.loc[:, "weight"]
            if cost:
                df_.loc[:, "z_shaped_cost"] = \
                    d.loc[i, cost_f].copy() * df_.loc[:, "weight"]

            df_ = df_.drop(columns=["weight"])

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

            paths = d.loc[:, path_f].apply(lambda s: s.split(sp))\
                .values
            dates = d.loc[:, path_dates].apply(lambda s: s.split(
                sp)).values
            c_dates = d.loc[:, conv_dates].values

            # iterate through the paths and calculate the linear touch
            # model
            for i, (path, date, c_date) in enumerate(zip(paths, dates,
                                                         c_dates)):
                features = [
                    "channel",
                    "time_decay_conversions"
                ]

                if rev:
                    features.append("time_decay_revenue")
                if cost:
                    features.append("time_decay_cost")

                # dataframe to hold the results of this iteration
                df_ = pd.DataFrame(columns=features)

                # add the channels to the dataframe
                for j, (channel, dt) in enumerate(zip(path, date)):
                    df_.loc[j, "channel"] = channel
                    # calculate the days before conversion for each
                    # channel
                    df_.loc[j, "dbc"] = (
                        np.datetime64(c_date) - np.datetime64(dt)
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
