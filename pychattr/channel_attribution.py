import ctypes

import pandas as pd


class PyChAttr(object):
    def __init__(self, df=None, model_type="markov",
                 model_paradigm=None, path_feature=None,
                 conversion_feature=None,
                 conversion_value_feature=None, null_path_feature=None,
                 separator=">", order=1, n_simulations=None,
                 max_step=None, return_transition_probs=False,
                 random_state=None):
        """

        Parameters
        ----------
        df : pandas.DataFrame containing the preprocessed path data.

        model_type : str; one of {'markov', 'heuristic'};
          default='markov'; required.

          the type of channel attribution model to construct.

        model_paradigm :  str or None; one of {'first_touch',
          'last_touch', 'linear', None}; default=None; required.

          the type of modeling paradigm to use.

          the 'first_touch', 'last_touch' and 'linear' paradigms can
          only be specified when `model_type='heuristic'` and
          subsequently, when using `model_type='markov'` this value
          must be set to None.

        path_feature : str; default=None; required.
          the name of the column in df containing the paths.

        conversion_feature : str; default=None; required.
          the name of the column in df containing the total
          conversions for each path.

        conversion_value_feature : str; default=None; optional.
          the name of the column in df containing the total
          conversion value for each path.

        null_path_feature : str; default=None; optional.
          the name of the column in df containing the paths that do
          not lead to conversion.

        separator : str; default='>'.
          symbol used to denote transition from one path to the next.

        order : int; default=1.
          denotes the order of the Markov model when
          `model_type='markov'`, ignored otherwise.

        n_simulations : one of {int, None}; default=None;
          total simulations from the transition matrix.

        max_step : one of {int, None}; default=None; optional.
          the maximum number of steps for a single simulated path.

        return_transition_probs : bool; default=True; required.
          whether to return the transition probabilities between
          channels and removal effects.

        random_state : one of {int, None}; default=None; optional.
          the seed used by the random number generator; ensures
          reproducibility between runs when specified.


        """
        self.df = df
        self.model_type = model_type
        self.model_paradigm = model_paradigm
        self.path_feature = path_feature
        self.conversion_feature = conversion_feature
        self.conversion_value_feature = conversion_value_feature
        self.null_path_feature = null_path_feature
        self.separator = separator
        self.order = order
        self.n_simulations = n_simulations
        self.max_step = max_step
        self.return_transition_probs = return_transition_probs
        self.random_state = random_state

    def fit(self, X, y):
        """fit the dataframe and produce the model."""

        # light input param validation
        self._validate_params()

        # markovian model
        if self.model_type == "markov":
            pass

        # one of {first_touch, last_touch, linear}
        if self.model_type == "heuristic":
            pass

    def predict(self, X):
        pass

    def _validate_params(self):
        """Lightweight validation effort."""
        # model_type
        if self.model_type not in ["markov", "heuristic"]:
            raise ValueError("`model_type` must be one of {'markov', "
                             "'heuristic'}")

        # validate by model_type
        if self.model_type == "markov":
            # model_paradigm must align with model_type
            if self.model_paradigm != None:
                raise ValueError("`model_paradigm` must be None when "
                                 "using 'markov' `model_type`")

        if self.model_type == "heuristic":
            # model_paradigm
            if self.model_paradigm not in \
                    ["first_touch", "last_touch", "linear"]:
                raise ValueError("`model_paradigm` must be one of "
                                 "{None, 'first_touch', 'last_touch', "
                                 "'linear'")

        # check the separator is the appropriate length
        if len(self.separator) != 1:
            raise ValueError("`separator` must have length 1")

    def _heuristic_model(self):
        pass

    def _markov_model(self):
        pass





