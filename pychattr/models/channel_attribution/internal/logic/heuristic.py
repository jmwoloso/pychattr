import functools

import numpy as np
import pandas as pd


def ensemble_results(paths, conversions, revenues, costs, separator):
    """Blended version of all the selected heuristic models."""
    raise NotImplementedError("This model specification will be "
                              "available in the next minor "
                              "release of pychattr.")

def fit_model(df, heuristic, paths, conversions, sep, revenues=None,
              costs=None, exclude_direct=False, direct_channel=None,
              lead_channel=None, oppty_channel=None, decay_rate=7,
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
            p = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).values
        else:
            p = df.loc[:, path_f].values

        # iterate through the paths and calculate the linear touch model
        for i in range(len(p)):
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
            p = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).values
        else:
            p = df.loc[:, path_f].values

        # iterate through the paths and calculate the u-shaped model
        for i in range(len(p)):
            # split the current path into individual channels
            channels = pd.Series(p[i]).apply(
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

            weight = 0.2 / len(idx)

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
                0.4
            # the remaining channels split 20%
            d_.loc[idx, "u_shaped_conversions"] *= weight

            if has_rev:
                d_.loc[:, "u_shaped_revenue"] = \
                    df.loc[i, rev_f].copy()
                d_.loc[[first_idx, last_idx], "u_shaped_revenue"] *= \
                    0.4
                d_.loc[idx, "u_shaped_revenue"] *= weight

            if has_cost:
                d_.loc[:, "u_shaped_cost"] = \
                    df.loc[i, cost_f].copy()
                d_.loc[[first_idx, last_idx], "u_shaped_cost"] *= \
                    0.4
                d_.loc[idx, "u_shaped_cost"] *= weight

            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def w_shaped(df, path_f, conv_f, sep, lead_channel, rev_f=None,
                 cost_f=None,exclude_direct=False, direct_channel=None):
        """W-shaped attribution model."""
        # container to hold the resulting dataframes
        results = []

        # aggregations to perform prior to sending results back
        aggs = {
            "w_shaped_conversions": "sum"
        }

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if has_rev:
            aggs["w_shaped_revenue"] = "sum"

        if has_cost:
            aggs["w_shaped_cost"] = "sum"

        if exclude_direct:
            p = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).values
        else:
            p = df.loc[:, path_f].values

        # iterate through the paths and calculate the u-shaped model
        for i in range(len(p)):
            # split the current path into individual channels
            channels = pd.Series(p[i]).apply(
                lambda s: np.array(s.split(sep))
            ).values[0]

            # cutoff the path after the oppty channel
            channels = channels[:np.argmax(
                channels == oppty_channel) + 1]

            # get the index where there lead channel resides
            lead_idx = np.argmax(channels == lead_channel)

            # get the indices of the channels to apply weights
            # appropriately
            idx = list(range(len(channels)))

            # remove the lead channel index
            idx.pop(lead_idx)

            # capture the first index
            first_idx = idx[0]
            # remove it from the list
            idx.pop(0)

            # capture the last index
            last_idx = idx[-1]
            # remove it from the list
            idx.pop(-1)

            weight = 0.1 / len(idx)

            # dataframe to hold the values for each channel for this
            # iteration
            d_ = pd.DataFrame({
                "channel": channels
            })

            # transfer over the values first
            d_.loc[:, "u_shaped_conversions"] = \
                df.loc[i, conv_f].copy()
            # now apply the correct weights; first and last get 40%
            d_.loc[[first_idx, lead_idx, last_idx],
                   "u_shaped_conversions"] *= 0.3
            # the remaining channels split 20%
            d_.loc[idx, "u_shaped_conversions"] *= weight

            if has_rev:
                d_.loc[:, "u_shaped_revenue"] = \
                    df.loc[i, rev_f].copy()
                d_.loc[[first_idx, lead_idx, last_idx],
                       "u_shaped_revenue"] *= 0.3
                d_.loc[idx, "u_shaped_revenue"] *= weight

            if has_cost:
                d_.loc[:, "u_shaped_cost"] = \
                    df.loc[i, cost_f].copy()
                d_.loc[[first_idx, lead_idx, last_idx],
                       "u_shaped_cost"] *= 0.3
                d_.loc[idx, "u_shaped_cost"] *= weight

            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def z_shaped(df, path_f, conv_f, sep, lead_channel, oppty_channel,
                 rev_f=None, cost_f=None, exclude_direct=False,
                 direct_channel=None):
        """Z-shaped (full path) attribution model."""
        # container to hold the resulting dataframes
        results = []

        # aggregations to perform prior to sending results back
        aggs = {
            "w_shaped_conversions": "sum"
        }

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if has_rev:
            aggs["w_shaped_revenue"] = "sum"

        if has_cost:
            aggs["w_shaped_cost"] = "sum"

        if exclude_direct:
            p = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).values
        else:
            p = df.loc[:, path_f].values

        # iterate through the paths and calculate the u-shaped model
        for i in range(len(p)):
            # split the current path into individual channels
            channels = pd.Series(p[i]).apply(
                lambda s: np.array(s.split(sep))
            ).values[0]

            # cutoff the path after the oppty channel
            channels = channels[:np.argmax(
                channels == oppty_channel) + 1]

            # get the index where there lead channel resides
            lead_idx = np.argmax(channels == lead_channel)
            oppty_idx = np.argmax(channels == oppty_channel)

            # get the indices of the channels to apply weights
            # appropriately
            idx = list(range(len(channels)))

            # remove the lead channel index
            idx.pop(lead_idx)
            idx.pop(oppty_idx)

            # capture the first index
            first_idx = idx[0]
            # remove it from the list
            idx.pop(0)

            # capture the last index
            last_idx = idx[-1]
            # remove it from the list
            idx.pop(-1)

            weight = 0.1 / len(idx)

            # dataframe to hold the values for each channel for this
            # iteration
            d_ = pd.DataFrame({
                "channel": channels
            })

            # transfer over the values first
            d_.loc[:, "u_shaped_conversions"] = \
                df.loc[i, conv_f].copy()
            # now apply the correct weights
            d_.loc[[first_idx, lead_idx, oppty_idx, last_idx],
                   "u_shaped_conversions"] *= 0.225
            # the remaining channels split 20%
            d_.loc[idx, "u_shaped_conversions"] *= weight

            if has_rev:
                d_.loc[:, "u_shaped_revenue"] = \
                    df.loc[i, rev_f].copy()
                d_.loc[[first_idx, lead_idx, oppty_idx, last_idx],
                       "u_shaped_revenue"] *= 0.225
                d_.loc[idx, "u_shaped_revenue"] *= weight

            if has_cost:
                d_.loc[:, "u_shaped_cost"] = \
                    df.loc[i, cost_f].copy()
                d_.loc[[first_idx, lead_idx, oppty_idx, last_idx],
                       "u_shaped_cost"] *= 0.225
                d_.loc[idx, "u_shaped_cost"] *= weight

            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    def time_decay(df, path_f, conv_f, sep, path_dates, conv_dates,
                   decay_rate=7, rev_f=None, cost_f=None,
                   exclude_direct=False, direct_channel=None):
        """Time decay attribution model."""
        def get_weight(days_to_conversion, decay_rate):
            """Takes the days-to-conversion and calculates the
            attribution weight using the decay rate supplied."""
            return np.exp2(-days_to_conversion / decay_rate)

        # container to hold the resulting dataframes
        results = []

        # aggregations to perform prior to sending results back
        aggs = {
            "time_decay_conversions": "sum"
        }

        has_rev = True if rev_f in df.columns else False
        has_cost = True if cost_f in df.columns else False

        if has_rev:
            aggs["time_decay_revenue"] = "sum"

        if has_cost:
            aggs["time_decay_cost"] = "sum"

        p = df.loc[:, path_f].values

        # iterate through the paths and calculate the u-shaped model
        for i in range(len(p)):
            # split the current path into individual channels
            channels = pd.Series(p[i]).apply(
                lambda s: np.array(s.split(sep))
            ).values[0]

            # split the current path dates into individual dates
            path_dates = df.loc[i, path_dates].apply(
                lambda s: np.array(s.split(sep))
            ).values[0]

            # get the conversion date
            conv_date = df.loc[i, conv_dates].values[0]

            # get the conversion
            conv = df.loc[i, conv_f].values[0]

            # get the revenue for this particular path
            if has_rev:
                rev = df.loc[i, rev_f].values[0]
            if has_cost:
                cost = df.loc[i, cost_f].values[0]

            if exclude_direct:
                # get the index of the direct channel
                direct_idx = np.argmax(channels == direct_channel)
                # remove the direct channel
                c_ = list(channels).pop(direct_idx)
                channels = np.array(c_)
                # remove the corresponding date
                pd_ = list(path_dates).pop(direct_idx)
                path_dates = np.array(pd_)
            else:
                pass
            # dataframe to hold the values for each channel for this
            # iteration
            d_ = pd.DataFrame({
                "channel": channels,
                "path_date": path_dates,
                "conv_date": [conv_date] * len(path_dates),
                "decay_rate": [decay_rate] * len(path_dates),
            })

            # calculate the days to conversion
            d_.loc[:, "dtc"] = (
                d_.loc[:, "conv_date"].astype("datetime64[ns]") -\
                d_.loc[:, "path_date"].astype("datetime64[ns]")
            ) / np.timedelta64(1, "D")

            d_ = d_.drop(columns=["conv_date", "path_date"])

            # calculate the conversions based on the decay rate for
            # each channel
            d_.loc[:, "time_decay_conversions"] = \
                np.vectorize(get_weight)(d_.loc[:, "dtc"],
                                         d_.loc[:, "decay_rate"])*conv

            if has_rev:
                # calculate the conversions based on the decay rate for
                # each channel
                d_.loc[:, "time_decay_revenue"] = \
                    (np.vectorize(get_weight)
                     (d_.loc[:, "dtc"], d_.loc[:, "decay_rate"])) * rev

            if has_cost:
                # calculate the conversions based on the decay rate for
                # each channel
                d_.loc[:, "time_decay_cost"] = \
                    (np.vectorize(get_weight)
                     (d_.loc[:, "dtc"], d_.loc[:, "decay_rate"]))*cost

            results.append(d_)

        # combine the results
        df_ = pd.concat(results, axis=0)

        return df_.groupby(["channel"], as_index=False).agg(aggs)

    # TODO: is there a cleaner way to do this?
    # the explicitly-named models need extra parameters sent to them
    if heuristic == "w_shaped":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, lead_channel, rev_f=revenues,
                              cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)

    elif heuristic == "z_shaped":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, lead_channel, oppty_channel,
                              rev_f=revenues, cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)

    elif heuristic == "time_decay":
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, path_dates, conv_dates,
                              decay_rate=decay_rate, rev_f=revenues,
                              cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)

    else:
        f = functools.partial(eval(heuristic), df, paths, conversions,
                              sep, rev_f=revenues, cost_f=costs,
                              exclude_direct=exclude_direct,
                              direct_channel=direct_channel)
    return f
