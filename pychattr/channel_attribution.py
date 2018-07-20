import ctypes
import pymc3
import networkx as nx
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from pomegranate import State, HiddenMarkovModel
from pomegranate.distributions import DiscreteDistribution
from rpy2.robjects import pandas2ri, r, NULL
from rpy2.robjects.vectors import DataFrame
from rpy2.robjects.packages import importr, data
from rpy2.robjects.lib import ggplot2


class PyChAttr(object):
    def __init__(self, df=None, model_type="both",
                 model_paradigm=None, path_feature=None,
                 conversion_feature=None,
                 conversion_value_feature=None, null_path_feature=None,
                 separator=">", order=1, n_simulations=None,
                 max_step=None, return_transition_probs=True,
                 random_state=None):
        """

        Parameters
        ----------
        df : pandas.DataFrame containing the preprocessed path data.

        model_type : str; one of {'markov', 'heuristic', 'both'};
          default='both'; required.

          the type of channel attribution model to construct.

        model_paradigm :  str or None; one of {'first_touch',
          'last_touch', 'linear', 'all_heuristics', 'markov', 'all'};
          default='all'; required.

          the type of modeling paradigm to use.

          the 'first_touch', 'last_touch', 'linear' and 'all_heuristics'
          paradigms will are used with `model_type='heuristic'`.

          the `markov` paradigm will be used when `model_type='markov'`.

          the `all` paradigm will be used when `model_type='both'` and
          will be the combination of the above.

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

    def fit(self):
        """fit the dataframe and produce the model."""

        # light input param validation
        self._validate_params()

        # turn on conversion
        pandas2ri.activate()

        # load the appropriate R packages
        baseR = importr("base")
        ChannelAttributionR = importr("ChannelAttribution")
        reshapeR = importr("reshape")
        ggplot2R = importr("ggplot2")

        r_packages = [
            baseR,
            ChannelAttributionR,
            reshapeR,
            ggplot2R
        ]

        # convert the pandas.DataFrame to an R Vector List
        # adds two new attrs self.r_list_ and self.r_model_params_
        self._python_params_to_r_objects(r_packages=r_packages)

        # if self.model_type == "both":
        #     self.models = list()
        #
        #     self._heuristic_model(r_packages=r_packages)
        #
        #     self.model_ = self._markov_model(r_packages=r_packages)
        #
        # # one of {first_touch, last_touch, linear} heuristic model
        # if self.model_type == "heuristic":
        #     self.model_ = self._heuristic_model(r_packages=r_packages)
        #
        # # markov model
        # if self.model_type == "markov":
        #     self.model_ = self._markov_model(r_packages=r_packages)

        return self

    # def transform(self):
    #     pass
    #
    # def fit_transform(self):
    #     pass

    def _validate_params(self):
        """Lightweight validation effort."""
        # model_type
        if self.model_type not in ["markov", "heuristic", "both"]:
            raise ValueError("`model_type` must be one of {'markov', "
                             "'heuristic', 'both'}")

        # validate by model_type
        if self.model_type == "both":
            if self.model_paradigm != "all":
                raise ValueError("`model_paradigm` must be 'all' "
                                 "when `model_type='both'`")
        if self.model_type == "markov":
            # model_paradigm must align with model_type
            if self.model_paradigm != "markov":
                raise ValueError("`model_paradigm` must be 'markov' "
                                 "when `model_type='markov'`")

        if self.model_type == "heuristic":
            # model_paradigm
            if self.model_paradigm not in \
                    ["first_touch", "last_touch", "linear",
                     "all_heuristics"]:
                raise ValueError("`model_paradigm` must be one of "
                                 "{'first_touch', 'last_touch', "
                                 "'linear', 'all_heuristics'} when"
                                 "`model_type='heuristic'`")

        # check the separator is the appropriate length
        if len(self.separator) != 1:
            raise ValueError("`separator` must have length 1")



    def _python_params_to_r_objects(self, r_packages=None):
        """Converts python objects to the appropriate R objects."""
        # get the base R namespace
        baseR = r_packages[0]

        # convert the pandas.DataFrame to an R list
        self.r_list_ =  baseR.split(DataFrame(self.df),
                           baseR.seq(baseR.nrow(DataFrame(self.df))))

        # convert the model params to strings in R
        self.r_model_params_ = {
            "path_feature": baseR.toString(self.path_feature),
            "conversion_feature":
                baseR.toString(self.conversion_feature),
            "conversion_value_feature":
                baseR.toString(self.conversion_value_feature),
            "null_path_feature": baseR.toString(self.null_path_feature),
            "separator": baseR.toString(self.separator),
            "order": baseR.toString(self.order),
            "n_simulations": baseR.toString(self.n_simulations),
            "max_step": baseR.toString(self.max_step),
            "return_transition_probs":
                baseR.as_logical(self.return_transition_probs),
            "random_state": baseR.as_integer(self.random_state) if
            self.random_state != None else NULL
        }

        return self



    @classmethod
    def _heuristic_model(cls, r_list=None, path_feature=None,
                         conversion_feature=None,
                         conversion_value_feature=None,
                         separator=None, r_packages=None):
        """Creates the heuristic models."""

        """
        self, df=None, path_feature=None,
                         conversion_feature=None,
                         conversion_value_feature=None,
                         separator=None
        """
        baseR = r_packages[0]
        ChannelAttribution = r_packages[1]
        reshapeR = r_packages[2]
        ggplot2R = r_packages[3]

        model = ChannelAttribution.heuristic_model(
            r_list,


        )


    @classmethod
    def _markov_model(cls, r_list=None, path_feature=None,
                      conversion_feature=None,
                      conversion_value_feature=None,
                      null_path_feature=None, model_order=1,
                      n_simulations=None, max_step=None,
                      return_transition_matrix=None, separator=None,
                      random_state=None, r_packages=None):
        """Creates the hidden markov models."""

        """
        df=None, path_feature=None,
                      conversion_feature=None,
                      conversion_value_feature=None,
                      null_path_feature=None, model_order=1,
                      n_simulations=None, max_step=None,
                      return_transition_matrix=None, separator=None
        """
        pass






