"""
Mixin classes containing common functionality for the various model
specifications.
"""
# Author: Jason Wolosonovich <jason@refinerynet.com>
# License: BSD 3-clause

import abc


class AttributionModelBase(metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, separator=">",
                 return_summary=False):
        self.paths = path_feature
        self.conversions = conversion_feature
        self.nulls = null_feature
        self.revenues = revenue_feature
        self.costs = cost_feature
        self.sep = separator
        self.summary = return_summary

    def fit(self, df):
        """
        Fit the specified model.

        Parameters
        ----------
        df: pandas.DataFrame; required.
          NOTE: Each row in the DataFrame should contain a single
          path. Aggregation among paths will be handled during the
          model-fitting process.

        Returns
        -------
        self
        """

        self._df = df.copy()

        # used in various places by both models
        self._has_rev = True if self.revenues else False
        self._has_cost = True if self.costs else False

        return self


class HeuristicModelMixin(AttributionModelBase, metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, separator=">",
                 return_summary=False, first_touch=True,
                 last_touch=True, linear_touch=True,
                 ensemble_results=True):

        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         separator=separator,
                         return_summary=return_summary)

        self.first = first_touch
        self.last = last_touch
        self.linear = linear_touch
        self.ensemble = ensemble_results

    def fit(self, df):
        super().fit(df)

        self._get_heuristics()

        # aggregate by path
        if df.loc[:, self.paths].max() == 1:
            self._aggregate_paths(self._df)

        return self

    def _aggregate_paths(self, df):
        """Aggregate the unique paths."""
        aggs = {
            self.conversions: "sum"
        }

        if self._has_rev:
            aggs[self.revenues] = "sum"
        if self._has_cost:
            aggs[self.costs] = "sum"

        # aggregate the values by path
        gb = df.groupby([self.paths], as_index=False).agg(aggs)

        # split the paths into lists of channels
        gb.loc[:, self.paths] = gb.loc[:, self.paths].apply(
            lambda s: s.split(self.sep)
        )

        # remove whitespace around channel names
        gb.loc[:, self.paths] = gb.loc[:, self.paths].apply(
            lambda s: [ss.strip() for ss in s]
        )

        self._df = gb.copy()

        return self

    def _get_heuristics(self):
        """Get the heuristic models to build."""
        heuristics = []
        if self.first:
            heuristics.append("first_touch")
        if self.last:
            heuristics.append("last_touch")
        if self.linear:
            heuristics.append("linear_touch")
        if self.ensemble:
            heuristics.append("ensemble")

        # set an attribute for the models to create
        self._heuristics = heuristics

        return self


class MarkovModelMixin(AttributionModelBase, metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, separator=">",
                 return_summary=False, k_order=1, n_simulations=10000,
                 max_steps=None, return_transition_probs=True,
                 random_state=None):
        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         separator=separator,
                         return_summary=return_summary)

        self.order = k_order
        self.n_sim = n_simulations
        self.max_steps = max_steps
        self.trans_probs = return_transition_probs
        self.random_state = random_state

    def fit(self, df):
        super().fit(df)

        return self
