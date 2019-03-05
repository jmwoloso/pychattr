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
      binary/boolean.

    revenue_feature: string; default=None; optional.
      The name of the feature containing the revenue generated
      for each path.

      NOTE: The values contained within this feature
      must be numeric.

    cost_feature: string; default=None; optional.
      The name of the feature containing the cost incurred for
      each path.

      NOTE: The values contained within this feature must
      be numeric.

    separator: string; default=">>>"; required.
      The symbol used to separate the channels in each path.

    first_touch: boolean; default=True.
      Whether to calculate the first-touch heuristic model.

    last_touch: boolean; default=True.
      Whether to calculate the last-touch heuristic model.

    linear_touch: boolean; default=True.
      Whether to calculate the linear-touch heuristic model.

    u_shaped: boolean; default=False.
      Whether to calculate the u-shaped heuristic model, also known as
      the position-based model. This model is typically used when the
      conversion event represents lead-creation.

    w_shaped: boolean; default=False.
      Whether to calculate the w-shaped heuristic model. This model is
      typically used when the paths contain the lead-creation and
      opportunity-creation stages.

      NOTE: When using this model the `lead_channel` parameter must be
      set to ensure the weights are applied correctly.

    z_shaped: boolean; default=False.
      Whether to calculate the z-shaped heuristic model, also known as
      the full-path model. This model is typically used to measure the
      full path from first-touch to the customer-close stage.

      NOTE: When using this model the `opportunity_stage` parameter
      must be set to ensure the weights are applied correctly.

    time_decay: boolean; default=False.
      Whether to calculate the time-decay heuristic model. This model
      assigns more credit to channels that occur closer to the
      conversion event. By nature, this model will downplay the
      importance of the top-of-funnel channels.

      NOTE: When specifying the time decay model, the
      `path_dates_feature` and `conversion_dates_feature` parameters
      must be set as they are used to calculate the number of days
      between the channel event and the conversion event during
      model-fitting. Additionally, the `lead_channel` and
      `opportunity_stage` parameters will be checked and applied if
      found.

    ensemble_results: boolean; default=True.
      Whether to create an ensemble of the resulting models.

    exclude_direct: boolean; default=False; optional.
      Whether to exclude the direct channel during the model fitting
      process. If `True`, then `direct_channel` must be specified.

    direct_channel: string; default=None; required if
      `last_touch_non_direct=True`.
      The name of the direct channel within the paths of the dataset.

    lead_channel: string; default=None; required if `w_shaped=True`.
      The name of the channel representing lead-creation within the
      paths of the dataset.

    opportunity_channel: string; default=None; required if
      `z_shaped=True`.
      The name of the channel representing opportunity-creation within
      the paths of the dataset.

    half_life: int; default=7; ignored if `time_decay=False`.
      The number of days to use in calculating the weights for each
      channel. The smaller the number, the smaller the amount of
      credit that earlier channels in the path will receive.

    path_dates_feature: string; default=None; required if
     `time_decay=True`.
      The name of the feature representing the dates of each event
      within the paths.

      NOTE: The format for the values in this feature are expected to
      be constructed according to the following format:
        for a given path (e.g. "A>>B>>C") corresponding dates might look
        like: "2019-01-01>>>2019-02-01>>>2019-03-01" where the separator
        is the same as that used to construct the paths.

    conversion_dates_feature: string; default=None; required if
      `time_decay=True`.
      The name of the feature representing the dates of the
      conversion event within the paths.

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
    https://support.google.com/analytics/answer/1662518?hl=en
    """
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 separator=">>>", first_touch=True, last_touch=True,
                 linear_touch=True, u_shaped=False, w_shaped=False,
                 z_shaped=False, time_decay=False,
                 ensemble_results=True, exclude_direct=False,
                 direct_channel=None, lead_channel=None,
                 opportunity_channel=None, half_life=7,
                 path_dates_feature=None,
                 conversion_dates_feature=None):
        super().__init__(path_feature, conversion_feature,
                         revenue_feature, cost_feature, separator)

        self.first = first_touch
        self.last = last_touch
        self.linear = linear_touch
        self.u = u_shaped
        self.w = w_shaped
        self.z = z_shaped
        self.time = time_decay
        self.ensemble = ensemble_results
        self.direct = exclude_direct
        self.direct_channel = direct_channel
        self.lead_channel = lead_channel
        self.oppty_channel = opportunity_channel
        self.half_life = half_life
        self.path_dates = path_dates_feature
        self.conv_dates = conversion_dates_feature

    def fit(self, df):
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
            self.sep,
            revenues=self.revenues,
            costs=self.costs,
            exclude_direct=self.direct,
            direct_channel=self.direct_channel,
            lead_channel=self.lead_channel,
            oppty_channel=self.oppty_channel,
            half_life=self.half_life,
            path_dates=self.path_dates,
            conv_dates=self.conv_dates
        )

        return self
