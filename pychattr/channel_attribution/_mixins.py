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
                 revenue_feature=None, cost_feature=None,
                 path_dates_feature=None, conversion_dates_feature=None,
                 direct_channel=None, exclude_direct=False,
                 separator=">>>", return_summary=False):
        print("AttributionModelBase instantiated.")
        self.paths = path_feature
        self.conversions = conversion_feature
        self.revenues = revenue_feature
        self.costs = cost_feature
        self.path_dates = path_dates_feature
        self.conv_dates = conversion_dates_feature
        self.direct = direct_channel
        self.exclude_direct = exclude_direct
        self.sep = separator
        self.summary = return_summary

    @abc.abstractmethod
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
        print("AttributionModelBase.fit() called.")
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
        pass


class HeuristicModelMixin(AttributionModelBase, metaclass=abc.ABCMeta):
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 path_dates_feature=None, conversion_dates_feature=None,
                 direct_channel=None, exclude_direct=False,
                 separator=">>>", return_summary=False,
                 lead_channel=None, opportunity_channel=None,
                 first_touch=True, last_touch=True,
                 linear_touch=True, u_shaped=False, w_shaped=False,
                 z_shaped=False, time_decay=False,
                 ensemble_results=True,  time_decay_days=7):

        super().__init__(path_feature, conversion_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         path_dates_feature=path_dates_feature,
                         conversion_dates_feature=conversion_dates_feature,
                         direct_channel=direct_channel,
                         exclude_direct=exclude_direct,
                         separator=separator,
                         return_summary=return_summary)
        print("HeuristicMixin instantiated.")

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

    @abc.abstractmethod
    def fit(self, df):
        print("HeuristicMixin.fit() called.")
        super().fit(df)
        print(self._idx_arr)
        print(type(self._idx_arr))

        self._get_heuristics()

        # if we're fitting a time decay model we also need to
        # remove the dates corresponding to the direct channel
        if "time_decay" in self._heuristics:
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

        return self

    def _get_heuristics(self):
        """Get the heuristic models to build."""
        # extensions
        print("HeuristicMixin._get_heuristics() called.")
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
            heuristics.append("ensemble_model")

        # set an attribute for the models to create
        self._heuristics = heuristics

        return self


class MarkovModelMixin(AttributionModelBase, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fit(self, df):
        super().fit(df)

    def _get_internals(self, df):
        """Extends the inherited method for markov-specific
        internals."""
        # aggregate the dataframe by path
        super()._get_internals(df)

        # create the transition matrix
        self.trans_mat = self._make_transition_matrix(self.df_,
                                                      self.paths)

    def _make_transition_matrix(self, df, path_f, sep=None,
                                exclude_direct=False,
                                direct_channel=None):
        """Calculate the transition probability matrix for the given
        paths."""
        # split the path strings into arrays containing each channel
        # in the path
        if exclude_direct:
            s_ = df.loc[:, path_f].str.replace(
                sep + "{}".format(direct_channel),
                "",
                regex=False
            ).apply(lambda s: np.array(s.split(sep))).values
        else:
            s_ = df.loc[:, path_f].apply(
                lambda s: np.array(s.split(sep))
            ).values

        return True