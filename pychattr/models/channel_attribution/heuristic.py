"""
heuristic.py: contains the class wrapper for the heuristic models 
used in channel attribution.

see: https://www.bizible.com/blog/multi-touch-attribution-full-debrief
"""

from .internal.utils import HeuristicModelMixin, \
    make_touch_point_dict, get_touch_point_values

from .internal.utils.heuristic import fit_heuristic_models


class HeuristicModel(HeuristicModelMixin):
    """
    Heuristic Channel attribution models.

    Parameters
    ----------
    path_feature: string; required.
      The name of the feature containing the paths.

    conversion_feature: string; required.
      The name of the feature containing the number of
      conversions for each path.

    revenue_feature: string; optional.
      The name of the feature containing the revenue generated
      for each path.

    cost_feature: string; optional.
      The name of the feature containing the cost incurred for
      each path.

    separator: string; required.
      The symbol used to separate the touch points in each path.

    first_touch: boolean; required.
      Whether to calculate the first-touch heuristic model.

    last_touch: boolean; required.
      Whether to calculate the last-touch heuristic model.

    linear_touch: boolean; required.
      Whether to calculate the linear-touch heuristic model.

    time_decay: boolean; required.
      Whether to calculate the time-decay heuristic model.

    u_shaped: boolean; required.
      Whether to calculate the u-shaped heuristic model.

    w_shaped: boolean; required.
      Whether to calculate the w-shaped heuristic model.

    z_shaped: boolean; required.
      Whether to calculate the z-shaped heuristic model.

    ensemble_results: boolean; required.
      Whether to create an ensemble of the resulting models.

    Attributes
    ----------
    # TODO: add attrs here

    Examples
    --------
    #TODO: add examples here

    See Also
    --------
    #TODO: add see also (if needed)

    Notes
    -----
    #TODO: add notes here (if needed)

    References
    ----------
    https://www.bizible.com/blog/multi-touch-attribution-full-debrief
    """
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 separator=">>>", first_touch=True,
                 last_touch=True, linear_touch=True, time_decay=True,
                 u_shaped=True, w_shaped=True, z_shaped=True,
                 ensemble_results=True):
        super().__init__(path_feature, conversion_feature,
                         revenue_feature, cost_feature, separator)

        self.first = first_touch
        self.last = last_touch
        self.linear = linear_touch
        self.time = time_decay
        self.u = u_shaped
        self.w = w_shaped
        self.z = z_shaped
        self.ensemble = ensemble_results

    def fit(self, df):
        """Fit the specified heuristic models."""
        # derive internal attributes that will be used during model
        # construction
        self._get_internals(df)

        # attempt to convert the values to the types required for
        # modeling
        #TODO: param/input validation

        # fit the specified heuristic models
        self.results_ = fit_heuristic_models(
            self._heuristics,
            self.df_,
            self.paths,
            self.conversions,
            self.revenues,
            self.costs,
            self.sep
        )

        return self



