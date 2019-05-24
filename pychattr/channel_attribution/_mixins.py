"""
Mixin classes containing common functionality for the various model
specifications.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause

import abc

import numpy as np


class AttributionModelBase(metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, path_date_feature=None,
                 conversion_date_feature=None, direct_channel=None,
                 exclude_direct=False, separator=">",
                 return_summary=False):

        self.paths = path_feature
        self.conversions = conversion_feature
        self.nulls = null_feature
        self.revenues = revenue_feature
        self.costs = cost_feature
        self.path_dates = path_date_feature
        self.conv_dates = conversion_date_feature
        self.direct = direct_channel
        self.exclude_direct = exclude_direct
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

        # if direct channels should be excluded, let's remove them now
        if self.exclude_direct:
            paths = self._df.loc[:, self.paths].apply(
                lambda s: np.array(s.split(self.sep))
            ).values

            # list to hold the indices of the direct for the time
            # decay model
            idxs = []
            # we'll reconstruct the path strings
            paths_ = []
            for path in paths:
                # find the indices corresponding to the direct channel
                idx = np.where(path == self.direct)[0]
                idxs.append(idx)

                # remove the direct channel elements
                path_ = np.delete(path, idx)

                # reconstruct the string
                path_ = "{}".format(self.sep).join(path_)

                paths_.append(path_)

            self._idx_arr = np.asarray(idxs)

            # make the replacements
            self._df.loc[:, self.paths] = paths_

        return self

    def _get_sales_summary(self):
        """Returns summary statistics about the sales cycle."""
        raise NotImplementedError("This feature will be available in "
                                  "a future release of pychattr.")


class HeuristicModelMixin(AttributionModelBase, metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, path_date_feature=None,
                 conversion_date_feature=None, direct_channel=None,
                 exclude_direct=False, separator=">",
                 return_summary=False, lead_channel=None,
                 opportunity_channel=None, first_touch=True,
                 last_touch=True, linear_touch=True, u_shaped=False,
                 w_shaped=False, z_shaped=False, time_decay=False,
                 ensemble_results=True,  time_decay_days=7):

        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         path_date_feature=path_date_feature,
                         conversion_date_feature=conversion_date_feature,
                         direct_channel=direct_channel,
                         exclude_direct=exclude_direct,
                         separator=separator,
                         return_summary=return_summary)

        self.lead = lead_channel
        self.oppty = opportunity_channel
        self.first = first_touch
        self.last = last_touch
        self.linear = linear_touch
        self.u = u_shaped
        self.w = w_shaped
        self.z = z_shaped
        self.decay = time_decay
        self.ensemble = ensemble_results
        self.decay_rate = time_decay_days

    def fit(self, df):
        super().fit(df)

        self._get_heuristics()

        # if we're fitting a time decay model we also need to
        # remove the dates corresponding to the direct channel
        if "time_decay" in self._heuristics and self.exclude_direct:
            dates = self._df.loc[:, self.path_dates].apply(
                lambda s: np.array(s.split(self.sep))
            ).values

            # we'll reconstruct the path strings
            dates_ = []
            for idx, date in zip(self._idx_arr, dates):
                print(date)
                # remove the direct channel elements
                date_ = np.delete(date, idx)

                # reconstruct the string
                date_ = "{}".format(self.sep).join(date_)

                dates_.append(date_)

            # make the replacements
            self._df.loc[:, self.path_dates] = dates_

        # aggregate by path
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
        if self.u:
            heuristics.append("u_shaped")
        if self.w:
            heuristics.append("w_shaped")
        if self.z:
            heuristics.append("z_shaped")
        if self.decay:
            heuristics.append("time_decay")
        if self.ensemble:
            heuristics.append("ensemble")

        # set an attribute for the models to create
        self._heuristics = heuristics

        return self


class MarkovModelMixin(AttributionModelBase, metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, path_date_feature=None,
                 conversion_date_feature=None, direct_channel=None,
                 exclude_direct=False, separator=">",
                 return_summary=False, k_order=1, n_simulations=10000,
                 max_steps=None, return_transition_probs=True,
                 random_state=None):

        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         path_date_feature=path_date_feature,
                         conversion_date_feature=conversion_date_feature,
                         direct_channel=direct_channel,
                         exclude_direct=exclude_direct,
                         separator=separator,
                         return_summary=return_summary)

        self.order = k_order
        self.n_sim = n_simulations
        self.max_steps = max_steps
        self.trans_probs = return_transition_probs
        self.random_state = random_state

    def fit(self, df):
        super().fit(df)

        # self._has_nulls = \
        #     True if self._df.loc[:, self.conversions].sum() != \
        #             self._df.shape[0] else False
        # if self._has_nulls:
            # calculate the conversion rate of the graph
            # self.graph_conv_rate = \
            #     self._df.loc[:, self.conversions].sum() / \
            #     self._df.shape[0]

        # # add markers for calculating transition probabilities
        # paths = self._df.loc[:, self.paths].values
        # paths_ = []
        #
        # for path in paths:
        #     start = ["START"]
        #     path.append("CONVERSION")
        #     path_ = start + path
        #     paths_.append(path_)
        #
        # self._df.loc[:, self.paths] = paths_

        return self
