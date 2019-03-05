import functools

import pandas as pd


def fit_model(df, heuristic, paths, conversions, sep, revenues=None,
              costs=None, exclude_direct=False, direct_channel=None,
              lead_channel=None, oppty_channel=None, half_life=7,
              path_dates=None, conv_dates=None):
    """Generates the specified heuristic model using partial
    application."""

    def first_touch(df, path_f, conv_f, sep, rev_f=None, cost_f=None,
                    exclude_direct=False, direct_channel=None):
        """First-touch attribution model."""
        df_ = pd.DataFrame(columns=["channel"])

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if exclude_direct:
            df_.loc[:, "channel"] = df.loc[:, path_f].str\
                .replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
                ).apply(lambda s: s.split(sep)[0])
        else:
            df_.loc[:, "channel"] = df.loc[:, path_f].apply(
                lambda s: s.split(sep)[0]
            )

        df_.loc[:, "first_touch_conversions"] = df.loc[:, conv_f].copy()
        if has_rev:
            df_.loc[:, "first_touch_revenue"] = df.loc[:, rev_f].copy()
        if has_cost:
            df_.loc[:, "first_touch_cost"] = df.loc[:, cost_f].copy()

        return df_

    def last_touch(df, path_f, conv_f, sep, rev_f=None, cost_f=None,
                   exclude_direct=False, direct_channel=None):
        """Last-touch attribution model."""
        df_ = pd.DataFrame(columns=["channel"])

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if exclude_direct:
            df_.loc[:, "channel"] = df.loc[:, path_f].str \
                .replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).apply(lambda s: s.split(sep)[-1])
        else:
            df_.loc[:, "channel"] = df.loc[:, path_f].apply(
                lambda s: s.split(sep)[-1]
            )

        df_.loc[:, "last_touch_conversions"] = df.loc[:, conv_f].copy()
        if has_rev:
            df_.loc[:, "last_touch_revenue"] = df.loc[:, rev_f].copy()
        if has_cost:
            df_.loc[:, "last_touch_cost"] = df.loc[:, cost_f].copy()

        return df_

    def linear_touch(df, path_f, conv_f, sep, rev_f=None, cost_f=None,
                     exclude_direct=False, direct_channel=None):
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

        if exclude_direct:
            paths = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).values
        else:
            paths = df.loc[:, path_f].values

        # iterate through the paths and calculate the linear touch model
        for i in range(len(paths)):
            # split the current path into individual channels
            channels = pd.Series(paths[i]).apply(
                lambda s: s.split(sep)
            )

            weight = 1 / len(channels)

            # dataframe to hold the values for each channel for this
            # iteration
            d_ = pd.DataFrame({
                "channel": channels
            })

            d_.loc[:, "linear_touch_conversions"] = \
                weight * df.loc[i, conv_f]

            if has_rev:
                d_.loc[:, "linear_touch_revenue"] = \
                    weight * df.loc[i, rev_f]

            if has_cost:
                d_.loc[:, "linear_touch_cost"] = \
                    weight * df.loc[i, cost_f]
            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def u_shaped(df, path_f, conv_f, sep, rev_f=None, cost_f=None,
                 exclude_direct=False, direct_channel=None):
        """U-shaped (position-based) attribution model."""
        # container to hold the resulting dataframes
        results = []

        # aggregations to perform prior to sending results back
        aggs = {
            "u_shaped_conversions": "sum"
        }

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if has_rev:
            aggs["u_shaped_revenue"] = "sum"

        if has_cost:
            aggs["u_shaped_cost"] = "sum"

        if exclude_direct:
            paths = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).values
        else:
            paths = df.loc[:, path_f].values

        # iterate through the paths and calculate the linear touch model
        for i in range(len(paths)):
            # split the current path into individual channels
            channels = pd.Series(paths[i]).apply(
                lambda s: s.split(sep)
            )

            # get the indices of the channels to apply weights
            # appropriately
            idx = list(range(len(channels)))

            # capture the first index
            first_idx = idx[0]
            # remove it from the list
            idx.pop(0)

            # capture the last index
            last_idx = idx[-1]
            # remove it from the list
            idx.pop(-1)

            weight1 = 0.2 / len(idx)
            weight2 = 0.4

            # dataframe to hold the values for each channel for this
            # iteration
            d_ = pd.DataFrame({
                "channel": channels
            })

            # transfer over the values first
            d_.loc[:, "u_shaped_conversions"] = \
                df.loc[i, conv_f].copy()
            # now apply the correct weights; first and last get 40%
            d_.loc[[first_idx, last_idx], "u_shaped_conversions"] *= \
                weight2
            # the remaining channels split 20%
            d_.loc[idx, "u_shaped_conversions"] *= weight1

            if has_rev:
                d_.loc[:, "u_shaped_revenue"] = \
                    df.loc[i, rev_f].copy()
                d_.loc[[first_idx, last_idx], "u_shaped_revenue"] *= \
                    weight2
                d_.loc[idx, "u_shaped_revenue"] *= weight1

            if has_cost:
                d_.loc[:, "u_shaped_cost"] = \
                    df.loc[i, cost_f].copy()
                d_.loc[[first_idx, last_idx], "u_shaped_cost"] *= \
                    weight2
                d_.loc[idx, "u_shaped_cost"] *= weight1

            # "fix" the first and last channel to meet their 40% share

            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def w_shaped(df, path_f, conv_f, sep, lead_channel, rev_f=None,
                 cost_f=None, exclude_direct=False,
                 direct_channel=None):
        """W-shaped attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def z_shaped(df, path_f, conv_f, sep, oppty_channel, rev_f=None,
                 cost_f=None, exclude_direct=False,
                 direct_channel=None):
        """Z-shaped (full path) attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def time_decay(df, path_f, conv_f, sep, path_dates, conv_dates,
                   lead_channel=None, oppty_channel=None, half_life=7,
                   rev_f=None, exclude_direct=False,
                   direct_channel=None):
        """Time decay attribution model."""
        # has_lead = True if lead_channel else False
        # has_oppty = True if oppty_channel else False
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def ensemble_model(paths, conversions, revenues, costs, separator):
        """Blended version of all the selected heuristic models."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    # TODO: is there a cleaner way to do this?
    # the first three models need extra parameters sent to them
    if heuristic == "time_decay":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, path_dates, conv_dates,
                              lead_channel=lead_channel,
                              oppty_channel=oppty_channel,
                              half_life=half_life, rev_f=revenues,
                              cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)

    elif heuristic == "w_shaped":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, lead_channel, rev_f=revenues,
                              cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)

    elif heuristic == "z_shaped":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, oppty_channel, rev_f=revenues,
                              cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)

    else:
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, rev_f=revenues, cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)
    return f
