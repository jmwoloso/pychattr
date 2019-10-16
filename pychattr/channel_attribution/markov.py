"""
Contains the class wrapper for the Markov model used in channel
attribution.
"""
# Author: Jason Wolosonovich <jason@refinerynet.com>
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

    separator: string; default=">>>"; required.
      The symbol used to separate the channels in each path.

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

    loops : bool; required; default=True.
      whether to estimate loops, i.e., going from state A
      to state A.

    Attributes
    ----------
    attribution_model_: The attribution model output.

    transition_matrix_: The transition probability matrix.

    removal_effects_: The removal effects for each channel.

    References
    ----------
    https://www.bizible.com/blog/multi-touch-attribution-full-debrief
    https://cran.r-project.org/web/packages/ChannelAttribution
    /ChannelAttribution.pdf

    """

    def __init__(self, path_feature, conversion_feature,
                 null_feature=None, revenue_feature=None,
                 cost_feature=None, separator=">>>", k_order=1,
                 n_simulations=10000, max_steps=None,
                 return_transition_probs=True, random_state=None, loops=True):
        super().__init__(path_feature, conversion_feature,
                         null_feature=null_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature,
                         separator=separator,
                         k_order=k_order, n_simulations=n_simulations,
                         max_steps=max_steps,
                         return_transition_probs=return_transition_probs,
                         random_state=random_state,
                         loops=loops)

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
            self.random_state,
            self.loops
        )

        self.attribution_model_ = df
        self.removal_effects_ = re_df
        self.transition_matrix_ = tmat

        return self
