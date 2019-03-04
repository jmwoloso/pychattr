"""
heuristic.py: contains the class wrapper for the heuristic models 
used in channel attribution.

see: https://www.bizible.com/blog/multi-touch-attribution-full-debrief
"""

from .internal.utils import HeuristicModelMixin

from .internal.utils.heuristic import fit_heuristic_models


class HeuristicModel(HeuristicModelMixin):
    """
    Heuristic Channel attribution models.

    Parameters
    ----------
    path_feature: string; required.
      The name of the feature containing the paths.

    conversion_feature: string; required.
      The name of the feature indicating whether the path resulted in a
      conversion.

      NOTE: The values contained within this feature must be
      boolean.

    revenue_feature: string; optional.
      The name of the feature containing the revenue generated
      for each path.

      NOTE: The values contained within this feature
      must be numeric.

    cost_feature: string; optional.
      The name of the feature containing the cost incurred for
      each path.

      NOTE: The values contained within this feature must
      be numeric.

    separator: string; required.
      The symbol used to separate the touch points in each path.

    first_touch: boolean; default=True; required.
      Whether to calculate the first-touch heuristic model.

    last_touch: boolean; required.
      Whether to calculate the last-touch heuristic model.

    linear_touch: boolean; required.
      Whether to calculate the linear-touch heuristic model.

    time_decay: boolean; required.
      Whether to calculate the time-decay heuristic model. This model
      assigns more credit to channels that occur closer to the
      conversion event. By nature, this model will downplay the
      importance of top-of-funnel channels.

    u_shaped: boolean; default=False; required.
      Whether to calculate the u-shaped heuristic model, also known as
      the position-based model. This model is typically used when the
      conversion event represents lead-creation.

    w_shaped: boolean; default=False required.
      Whether to calculate the w-shaped heuristic model. This model is
      typically used when the paths contain the lead-creation and
      opportunity-creation stages.

      NOTE: When using this model the `lead_stage` parameter must be
      set to ensure the weights are applied correctly.

    z_shaped: boolean; required.
      Whether to calculate the z-shaped heuristic model, also known as
      the full-path model. This model is typically used to measure the
      full path from first-touch to the customer-close stage.

      NOTE: When using this model the `opportunity_stage` parameter
      must be set to ensure the weights are applied correctly.

    ensemble_results: boolean; required.
      Whether to create an ensemble of the resulting models.

    half_life: int; default=7; ignored if `time_decay=False`.
      The number of days to use in calculating the weights for each
      channel. The smaller the number, the smaller the amount of
      credit that earlier channels in the path will receive.

    lead_stage: string; default=None; required if `w_shaped=True`.
      The name of the channel representing lead-creation within the
      paths of the dataset.

    opportunity_stage: string; default=None; required if
      `z_shaped=True`.

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
    https://www.bizible.com/blog/marketing-attribution-models-complete-list
    """
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 separator=">>>", first_touch=True,
                 last_touch=True, linear_touch=True, time_decay=False,
                 u_shaped=False, w_shaped=False, z_shaped=False,
                 ensemble_results=True, half_life=7, lead_stage=None,
                 opportunity_stage=None):
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
        self.half_life = half_life
        self.lead_stage = lead_stage
        self.oppty_stage = opportunity_stage

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
