import functools
import collections

import numpy as np
import pandas as pd


def fit_model(df, paths, conversions, revenues, costs,
              separator, heuristic="first_touch"):
    """Generates the specified heuristic model using partial
    application."""

    def first_touch_model(df, path_f, conv_f, sep, rev_f=None,
                          cost_f=None):
        """First-touch attribution model."""
        df_ = pd.DataFrame(columns=["channel"])

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        df_.loc[:, "channel"] = df.loc[:, path_f].apply(
            lambda s: s.split(sep)[0]
        )

        df_.loc[:, "first_touch_conversions"] = df.loc[:, conv_f].copy()
        if has_rev:
            df_.loc[:, "first_touch_revenue"] = df.loc[:, rev_f].copy()
        if has_cost:
            df_.loc[:, "first_touch_cost"] = df.loc[:, cost_f].copy()

        return df_

    def last_touch_model(df, path_f, conv_f, sep, rev_f=None,
                         cost_f=None):
        """Last-touch attribution model."""
        df_ = pd.DataFrame(columns=["channel"])

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        df_.loc[:, "channel"] = df.loc[:, path_f].apply(
            lambda s: s.split(sep)[-1]
        )

        df_.loc[:, "last_touch_conversions"] = df.loc[:, conv_f].copy()
        if has_rev:
            df_.loc[:, "last_touch_revenue"] = df.loc[:, rev_f].copy()
        if has_cost:
            df_.loc[:, "last_touch_cost"] = df.loc[:, cost_f].copy()

        return df_

    def linear_touch_model(df, path_f, conv_f, sep, rev_f=None,
                           cost_f=None):
        """Linear touch attribution model."""
        # container to hold the resulting dataframes
        results = []

        # aggregations to perform prior to sending results back
        aggs = {
            "linear_touch_conversions": "sum"
        }

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if has_rev:
            aggs["linear_touch_revenue"] = "sum"

        if has_cost:
            aggs["linear_touch_cost"] = "sum"

        paths = df.loc[:, path_f].values

        # iterate through the paths and calculate the linear touch model
        for i in range(len(paths)):
            # split the current path into individual channels
            channels = pd.Series(paths[i]).apply(
                lambda s: s.split(sep)
            )

            # dataframe to hold the values for each channel for this
            # iteration
            d_ = pd.DataFrame({
                "channel": channels
            })

            d_.loc[:, "linear_touch_conversions"] = \
                df.loc[i, conv_f] / len(channels)

            if has_rev:
                d_.loc[:, "linear_touch_revenue"] = \
                    df.loc[i, rev_f] / len(channels)

            if has_cost:
                d_.loc[:, "linear_touch_cost"] = \
                    df.loc[i, cost_f] / len(channels)
            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def time_decay_model(paths, conversions, revenues, costs, separator):
        """Time decay attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def u_shaped_model(paths, conversions, revenues, costs, separator):
        """U-shaped attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def w_shaped_model(paths, conversions, revenues, costs, separator):
        """W-shaped attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def z_shaped_model(paths, conversions, revenues, costs, separator):
        """Z-shaped (full path) attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def ensemble_model(paths, conversions, revenues, costs, separator):
        """Blended version of all the selected heuristic models."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    # TODO: is there a cleaner way to do this?
    f = "{}_model".format(heuristic)

    return functools.partial(eval(f), df, paths, conversions, separator,
                             rev_f=revenues, cost_f=costs)
