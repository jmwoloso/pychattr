from functools import partial


def fit_model(paths, conversions, revenues, costs,
              separator, heuristic="first_touch"):

    """Generates the specified heuristic model via the principle of
    partial application."""

    def first_touch_model(paths, conversions, revenues, costs, separator):
        """First-touch attribution model."""
        raise NotImplementedError("This model specification will be "
                                  "available in the next minor "
                                  "release of pychattr.")

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

    return partial(eval(f), paths, conversions, revenues, costs,
                   separator)
