import functools
import collections

import numpy as np
import pandas as pd


def fit_model(paths, conversions, revenues, costs,
              separator, heuristic="first_touch"):
    """Generates the specified heuristic model via the principle of
    partial application."""

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

    def last_touch_model(paths, conversions, revenues, costs, separator):
        """Last-touch attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

    def linear_touch_model(paths, conversions, revenues, costs, separator):
        """Linear touch attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

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

    return functools.partial(eval(f), paths, conversions, separator,
                             rev_f=revenues, cost_f=costs)
