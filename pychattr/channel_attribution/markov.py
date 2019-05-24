"""
Contains the class wrapper for the Markov model used in channel
attribution.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause

from ._mixins import MarkovModelMixin
from ._markov import fit_markov


class MarkovModel(MarkovModelMixin):
    """
    Markov channel attribution model.

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

    k_order : int; default=1.
      denotes the order, or "memory" of the Markov model.

    n_simulations : one of {int, None}; default=10000.
      total simulations from the transition matrix.

    max_steps : one of {int, None}; default=None.
      the maximum number of steps for a single simulated path.

    return_transition_probs : bool; required; default=True.
      whether to return the transition probabilities between
      channels and removal effects.

    random_state : one of {int, None}; optional; default=None.
      the seed used by the random number generator; ensures
      reproducibility between runs when specified.


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
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, path_date_feature=None,
                 conversion_date_feature=None, direct_channel=None,
                 exclude_direct=False, separator=">",
                 return_summary=False, k_order=1,
                 n_simulations=10000, max_steps=None,
                 return_transition_probs=True, random_state=None):

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
                         k_order=k_order, n_simulations=n_simulations,
                         max_steps=max_steps,
                         return_transition_probs=return_transition_probs,
                         random_state=random_state)

    def fit(self, df):
        """

        Parameters
        ----------
        df: pandas.DataFrame; required.
            The dataframe containing the path data to be modeled.

        Returns
        -------
        self: returns a fitted instance of self.
        """
        # derive the feature attributes and aggregate the dataset by
        # path
        super().fit(df)

        df, re_df, tmat = fit_markov(
            df,
            self.paths,
            self.conversions,
            self.revenues,
            self.nulls,
            self.n_sim,
            self.max_steps,
            self.trans_probs,
            self.sep,
            self.order,
            self.random_state
        )

        self.attribution_model_ = df
        self.removal_effects_ = re_df
        self.transition_matrix_ = tmat

        return self
