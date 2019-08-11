"""
Contains the class wrapper for the heuristic models used in channel
attribution.
"""
# Author: Jason Wolosonovich <jason@refinerynet.com>
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

    null_feature: string; default=None; optional.
      The name of the feature indicating whether the path resulted in a
      non-conversion.

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

    ensemble_results: boolean; default=True.
      Whether to create an ensemble of the resulting models.

    Attributes
    ----------
    attribution_model_: The attribution model output.

    References
    ----------
    https://www.bizible.com/blog/multi-touch-attribution-full-debrief
    https://www.bizible.com/blog/marketing-attribution-models
    -complete-list
    https://support.google.com/analytics/answer/1662518?hl=en
    https://www.optimizesmart.com/understanding-conversion-credit
    -distribution-attribution-models-google-analytics/
    https://docs.attributionapp.com/docs/time-decay-attribution
    -example-direct-included
    """

    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 null_feature=None, separator=">>>", first_touch=True,
                 last_touch=True, linear_touch=True,
                 ensemble_results=True):
        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         separator=separator,
                         first_touch=first_touch,
                         last_touch=last_touch,
                         linear_touch=linear_touch,
                         ensemble_results=ensemble_results)

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
            revenues=self.revenues,
            costs=self.costs,
            has_rev=self._has_rev,
            has_cost=self._has_cost
        )

        return self
