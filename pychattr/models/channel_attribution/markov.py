"""
markov.py: contains the class wrapper for the Markov model used in
channel attribution.
"""
from .internal import ChannelAttributionMixin


class MarkovModel(ChannelAttributionMixin):
    """
    Markov channel attribution model.

    Parameters
    ----------
    path_feature: string; required.
      The name of the feature containing the paths.

    conversion_feature: string; required.
      The name of the feature containing the number of
      conversions for each path.

    revenue_feature: string; optional; default=None.
      The name of the feature containing the revenue generated
      for each path.

    cost_feature: string; optional; default=None.
      The name of the feature containing the cost incurred for
      each path.

    separator: string; required; default=">>>"..
      The symbol used to separate the touch points in each path.

    markov_order : int; default=1.
      denotes the order, or "memory" of the Markov model.

    n_simulations : one of {int, None}; default=10000.
      total simulations from the transition matrix.

    max_step : one of {int, None}; default=None.
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
                 revenue_feature=None, cost_feature=None,
                 separator=">>>", markov_order=1, n_simulations=10000,
                 max_step=None, return_transition_probs=True,
                 random_state=None):
        super().__init__(path_feature, conversion_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature, separator=separator)
        self.order = markov_order
        self.n_sim = n_simulations
        self.max_step = max_step
        self.trans_probs = return_transition_probs
        self.random_state = random_state

    def fit(self, df):
        """

        Parameters
        ----------
        dataframe: pandas.DataFrame; required.
            The dataframe containing the path data to be modeled.

        Returns
        -------
        self: returns an instance of self.
        """
        # derive the feature attributes
        self._get_internals(df)
