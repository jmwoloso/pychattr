"""
Contains the class wrapper for the heuristic models used in channel
attribution.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause

from ._mixins import HeuristicModelMixin
from ._heuristic import fit_heuristic_models


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

      NOTE: When using Markov attribution, do not pre-aggregate
      conversions by path as this will effect the outcome of the
      simulation.

    null_feature: string; default=None; optional.
      The name of the feature indicating whether the path resulted in a
      non-conversion.

      NOTE: When using Markov attribution, do not pre-aggregate
      non-conversions by path as this will effect the outcome of the
      simulation.

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

    path_date_feature: string; default=None; required if
     `time_decay=True`.
      The name of the feature representing the dates of each event
      within the paths.

      NOTE: The format for the values in this feature are expected to
      be constructed according to the following format:
        for a given path (e.g. "A>>B>>C") corresponding dates might look
        like: "2019-01-01>>>2019-02-01>>>2019-03-01" where the separator
        is the same as that used to construct the paths.

    conversion_date_feature: string; default=None; required if
      `time_decay=True`.
      The name of the feature representing the date of the events found
      in `conversion_feature`.

    direct_channel: string; default=None; required if
    `exclude_direct=True`.
      The name of the direct channel within the paths of the dataset.

    exclude_direct: boolean; default=False; optional.
      Whether to exclude the direct channel during the model fitting
      process. If `True`, then `direct_channel` must be specified.

    separator: string; default=">>>"; required.
      The symbol used to separate the channels in each path.

    return_summary: boolean; default=False; optional.
      Whether the return summary statistics on the sales cycle for
      the given dataset.

      NOTE: both `path_date_feature` and `conversion_date_feature`
      must be specified as they are used during the calculation of
      summary statistics.

    first_touch: boolean; default=True.
      Whether to calculate the first-touch heuristic model.

    last_touch: boolean; default=True.
      Whether to calculate the last-touch heuristic model.

    linear_touch: boolean; default=True.
      Whether to calculate the linear-touch heuristic model.

    u_shaped: boolean; default=False.
      Whether to calculate the u-shaped heuristic model, also known as
      the position-based model. This model is typically used to gauge
      the effectiveness of lead-creation.

    w_shaped: boolean; default=False.
      Whether to calculate the w-shaped heuristic model. This model is
      typically used to gauge the effectiveness of opportunity-creation.

      NOTE: When using this model the `lead_channel` parameter must
      be set to ensure the weights are applied correctly to the lead
      channel.

    lead_channel: string; default=None; required if `w_shaped=True`
    or `z_shaped=True`.
      The name of the channel representing lead-creation within the
      paths of the dataset.

    z_shaped: boolean; default=False.
      Whether to calculate the z-shaped heuristic model, also known as
      the full-path model. This model is typically used to measure the
      full path from first-touch to the customer-close stage.

      NOTE: When using this model the `lead_channel` and
      `opportunity_channel` parameters must be set to ensure the
      weights are applied correctly to the lead and opportunity
      channels.

    opportunity_channel: string; default=None; required if
      `z_shaped=True`.
      The name of the channel representing the touch point directly
      before opportunity-creation within the paths of the dataset.

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

    time_decay_days: int; default=7; ignored if `time_decay=False`.
      The number of days to use in calculating the weights for each
      channel in the time decay model. The smaller the number,
      the smaller the amount of credit that earlier channels in the
      path will receive. For example, with the default value of 7
      days, an interaction that occurred 7 days prior to the
      conversion would receive 50% of the credit for the conversion.

    ensemble_results: boolean; default=True.
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
    https://www.bizible.com/blog/marketing-attribution-models-complete-list
    https://support.google.com/analytics/answer/1662518?hl=en
    https://www.optimizesmart.com/understanding-conversion-credit-distribution-attribution-models-google-analytics/
    https://docs.attributionapp.com/docs/time-decay-attribution-example-direct-included
    """
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, path_date_feature=None,
                 conversion_date_feature=None, direct_channel=None,
                 exclude_direct=False, separator=">",
                 return_summary=False, first_touch=True,
                 last_touch=True, linear_touch=True, u_shaped=False,
                 w_shaped=False, lead_channel=None, z_shaped=False,
                 opportunity_channel=None, time_decay=False,
                 time_decay_days=7, ensemble_results=True):

        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         path_date_feature=path_date_feature,
                         conversion_date_feature=conversion_date_feature,
                         direct_channel=direct_channel,
                         exclude_direct=exclude_direct,
                         separator=separator,
                         return_summary=return_summary,
                         lead_channel=lead_channel,
                         opportunity_channel=opportunity_channel,
                         first_touch=first_touch,
                         last_touch=last_touch,
                         linear_touch=linear_touch, u_shaped=u_shaped,
                         w_shaped=w_shaped, z_shaped=z_shaped,
                         time_decay=time_decay,
                         ensemble_results=ensemble_results,
                         time_decay_days=time_decay_days)

    def fit(self, df):
        # derive internal attributes that will be used during model
        # construction
        super().fit(df)

        # attempt to convert the values to the types required for
        # modeling
        # TODO: param/input validation

        # fit the specified heuristic models
        self.attribution_model_ = fit_heuristic_models(
            self._heuristics,
            self._df,
            self.paths,
            self.conversions,
            self.sep,
            revenues=self.revenues,
            costs=self.costs,
            lead_channel=self.lead,
            oppty_channel=self.oppty,
            decay_rate=self.decay_rate,
            path_dates=self.path_dates,
            conv_dates=self.conv_dates,
            has_rev=self._has_rev,
            has_cost=self._has_cost
        )

        return self
