import pandas as pd
from rpy2.robjects import pandas2ri, NULL
from rpy2.robjects.vectors import DataFrame as RDataFrame
from rpy2.robjects.packages import importr


class PyChAttr(object):
    def __init__(self, df=None, markov_model=True, heuristic_model=True,
                 first_touch=True, last_touch=True,
                 linear_touch=True, path_feature=None,
                 conversion_feature=None, conversion_value_feature=None,
                 null_path_feature=None, separator=">", order=1,
                 n_simulations=None, max_step=None,
                 return_transition_probs=True, random_state=None,
                 return_plot_data=True):
        """

        Parameters
        ----------
        df : pandas.DataFrame containing the preprocessed path data.

        markov_model : bool; whether to return the markov model;
          default=True; required.

        heuristic_model : bool; whether to return any of the models
          used traditionally in multi-touch attribution;
          default=True; required; ignored when `heuristic_model=False`.

        first_touch : bool; whether to return the first-touch
          attribution model; default=True; required; ignored when
          `heuristic_model=False`.

        last_touch : bool; whether to return the last-touch
          attribution model; default=True; required; ignored when
          `heuristic_model=False`.

        linear_touch : bool; whether to return the linear-touch
          attribution model; default=True; required; ignored when
          `heuristic_model=False`.

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

          NOTE: if specified, the feature name in the dataframe must be
          "total_null" or errors will occur within the underlying
          R library.

        separator : str; default='>'.
          symbol used to denote transition from one path to the next.

        order : int; default=1.
          denotes the order of the Markov model when
          `model_type='markov'`, ignored otherwise.

        n_simulations : one of {int, None}; default=None;
          total simulations from the transition matrix.

        max_step : one of {int, None}; default=None.
          the maximum number of steps for a single simulated path.

        return_transition_probs : bool; default=True; required.
          whether to return the transition probabilities between
          channels and removal effects.

        random_state : one of {int, None}; default=None.
          the seed used by the random number generator; ensures
          reproducibility between runs when specified.

        return_plot_data : bool; default=True.
          whether to return the melted datasets suitable for plotting.


        Attributes
        ----------
        r_df_: instance of `df` converted to an R DataFrame.

        model_: the fitted model.

        r_model_params_: dict mapping the PyChAttr parameters to their
          equivalent R function parameters.

        melted_data_ = list containing the melted conversion
          dataframe and the melted conversion value dataframe for
          plotting.

        """
        self.df = df
        self.markov_model = markov_model
        self.heuristic_model = heuristic_model
        self.first_touch = first_touch
        self.last_touch = last_touch
        self.linear_touch = linear_touch
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
        self.return_plot_data = return_plot_data

    def fit(self):
        """fit the dataframe and produce the model.

        Returns
        -------
        self
        """

        # light input param validation
        self._validate_params()

        # turn on pandas to ri conversion
        pandas2ri.activate()

        # load the appropriate R packages
        Rbase = importr("base")
        RChannelAttribution = importr("ChannelAttribution")

        # convert the pandas.DataFrame to an R Vector List
        # adds two new attrs self.r_list_ and self.r_model_params_
        self.r_df_, self.r_model_params_ = \
            self._python_params_to_r_objects(
                r_package=Rbase
            )

        # get the final feature subsets
        if self.conversion_value_feature is not None:
            self.conversion_features_, \
            self.conversion_value_features_ = \
                self._get_feature_subsets(
                    return_values=True
                )
        else:
            self.conversion_features_ = \
                self._get_feature_subsets(
                    return_values=False
                )

        # fit both types of models
        if self.markov_model is True & self.heuristic_model is True:
            # heuristic
            heuristic = \
                self._heuristic_models(r_package=RChannelAttribution)

            self.heuristic_ = heuristic.copy()

            # markov
            markov = self._markov_model(r_package=RChannelAttribution)

            if self.return_transition_probs is True:
                # separate and convert the sub-components
                self.transition_matrix_ = pandas2ri.ri2py(markov[1])
                self.removal_effects_ = pandas2ri.ri2py(markov[2])
                markov = pandas2ri.ri2py(markov[0])

                markov = markov.rename(
                    columns={
                        "total_conversions": "markov model",
                        "channel_name": "channel name"
                    }
                )
                if self.conversion_value_feature is not None:
                    markov = markov.rename(
                        columns={
                            "total_conversion_value": "markov value",
                            "channel_name": "channel name"
                        }
                    )
                self.markov_ = markov.copy()
            else:
                markov = markov.rename(
                    columns={
                        "total_conversions": "markov model",
                        "channel_name": "channel name"
                    }
                )
                if self.conversion_value_feature is not None:
                    markov = markov.rename(
                        columns={
                            "total_conversion_value": "markov value",
                            "channel_name": "channel name"
                        }
                    )
                self.markov_ = markov.copy()

            # TODO: parameterize "channel_name"?
            # combine the two models (they're just dataframes)
            self.model_ = pd.merge(heuristic.copy(),
                                   markov.copy(),
                                   on="channel name")

        # heuristic model only
        elif self.markov_model is False and self.heuristic_model is \
                True:
            self.heuristic_ = self.model_ = \
                self._heuristic_models(r_package=RChannelAttribution)

        # fit markov only
        elif self.markov_model is True and self.heuristic_model is \
                False:
            markov = \
                self._markov_model(r_package=RChannelAttribution)

            if self.return_transition_probs is True:
                # the conversion back to pandas needs to happen here
                self.transition_matrix_ = pandas2ri.ri2py(markov[1])
                self.removal_effects_ = pandas2ri.ri2py(markov[2])
                markov = pandas2ri.ri2py(markov[0])
                markov = markov.rename(
                    columns={
                        "total_conversions": "markov model",
                        "channel_name": "channel name"
                    }
                )
                if self.conversion_value_feature is not None:
                    markov = markov.rename(
                        columns={
                            "total_conversion_value": "markov value",
                            "channel_name": "channel name"
                        }
                    )
            else:
                markov = markov.rename(
                    columns={
                        "total_conversions": "markov model",
                        "channel_name": "channel name"
                    }
                )
                if self.conversion_value_feature is not None:
                    markov = markov.rename(
                        columns={
                            "total_conversion_value": "markov value",
                            "channel_name": "channel name"
                        }
                    )

            # assign the attributes
            self.markov_ = self.model_= markov.copy()

        if self.return_plot_data is True:
            self.melted_data_ = list()

            # add the melted conversion totals data
            self.melted_data_.append(
                pd.melt(
                    self.model_.loc[:,
                    self.conversion_features_].copy(),
                    id_vars=["channel name"],
                    var_name="model heuristic",
                    value_name="total conversions"
                )
            )
            if self.conversion_value_feature is not None:
                # add the melted conversion value data
                self.melted_data_.append(
                    pd.melt(
                        self.model_.loc[:,
                        self.conversion_value_features_].copy(),
                        id_vars=["channel name"],
                        var_name="model heuristic",
                        value_name="total conversion value"
                    )
                )

        return self

    def _validate_params(self):
        """Lightweight validation effort."""
        if self.markov_model not in [True, False]:
            raise ValueError("`markov_model` must be one of {True, "
                             "False}")

        if self.heuristic_model not in [True, False]:
            raise ValueError("`heuristic_model` must be one of {True, "
                             "False}")

        if self.markov_model & self.heuristic_model == False:
            raise ValueError("at least one of `markov_model` and "
                             "`heuristic_model` must be True")

        if self.heuristic_model is True:
            # if these are all False, raise
            if self.first_touch == self.last_touch == \
                    self.linear_touch == False:
                raise ValueError("must specify as True at least one of "
                                 "{`first_touch`, `last_touch`, "
                                 "`linear_touch`} when "
                                 "setting `heuristic_model=True`")

        if self.first_touch not in [True, False]:
            raise ValueError("`first_touch` must be one of {True, "
                             "False}")

        if self.last_touch not in [True, False]:
            raise ValueError("`last_touch` must be one of {True, "
                             "False}")

        if self.linear_touch not in [True, False]:
            raise ValueError("`linear_touch` must be one of {True, "
                             "False}")

        if self.path_feature is None:
            raise ValueError("`path_feature` must be specified.")

        if self.conversion_feature is None:
            raise ValueError("`conversion_feature` must be specified.")

        if self.return_transition_probs not in [True, False]:
            raise ValueError("`return_transition_probs` must be one "
                             "of {True, False}")

        if self.n_simulations is not None:
            if type(self.n_simulations) != int:
                raise ValueError("`n_simulations` must be one of {"
                                 "int, None}")

        if self.max_step is not None:
            if type(self.max_step) != int:
                raise ValueError("`max_step` must be one of {int, "
                                 "None}")

        if self.markov_model is True:
            if self.order is not None:
                if type(self.order) != int:
                    raise ValueError("`order` must be one of {int, "
                                     "None}")

        if self.conversion_value_feature is not None:
            if type(self.conversion_value_feature) != str:
                raise ValueError("`conversion_value_feature` should "
                                 "be one of {str, None}")

        if self.null_path_feature is not None:
            if type(self.null_path_feature) != str:
                raise ValueError("`null_path_feature` must be one of "
                                 "{str, None}")

        # check the separator is the appropriate length
        if len(self.separator) != 1:
            raise ValueError("`separator` must have length 1")

    def _get_feature_subsets(self, return_values=False):
        """Return the feature subsets depending on input params."""
        conversion_features = ["channel name"]
        conversion_value_features = ["channel name"]
        if self.first_touch is True:
            conversion_features.append("first touch")
        if self.last_touch is True:
            conversion_features.append("last touch")
        if self.linear_touch is True:
            conversion_features.append("linear touch")
        if return_values is True:
            if self.first_touch is True:
                conversion_value_features.append("first touch value")
            if self.last_touch is True:
                conversion_value_features.append("last touch value")
            if self.linear_touch is True:
                conversion_value_features.append("linear touch value")

        if self.markov_model is True:
            conversion_features.append("markov model")
            if return_values is True:
                conversion_value_features.append("markov value")
        if return_values is True:
            return conversion_features, conversion_value_features
        elif return_values is False:
            return conversion_features


    def _python_params_to_r_objects(self, r_package=None):
        """Converts python objects to the appropriate R objects."""

        # get a ref to base R namespace
        Rbase = r_package

        # convert the pandas.DataFrame to an R dataframe
        r_df_ = RDataFrame(self.df)

        # convert the model params to strings in R
        r_model_params_ = {
            "path_feature": Rbase.toString(self.path_feature),

            "conversion_feature":
                Rbase.toString(self.conversion_feature),

            "conversion_value_feature":
                Rbase.toString(self.conversion_value_feature)
                if self.conversion_value_feature is not None
                else NULL,

            "null_path_feature": Rbase.toString(self.null_path_feature)
                if self.null_path_feature is not None
                else NULL,

            "separator": Rbase.toString(self.separator),

            "order": Rbase.as_double(self.order),

            "n_simulations": Rbase.as_double(self.n_simulations)
                if self.n_simulations is not None
                else NULL,

            "max_step": Rbase.as_double(self.max_step)
                if self.max_step is not None
                else NULL,

            "return_transition_probs":
                Rbase.as_logical(self.return_transition_probs)
                if self.return_transition_probs is not None
                else NULL,

            "random_state": Rbase.as_double(self.random_state) if
            self.random_state != None else NULL
        }

        return r_df_, r_model_params_

    def _heuristic_models(self, r_package=None):
        """Creates the heuristic models."""
        # get a ref to the R package so we can call the function
        RChannelAttribution = r_package

        # keywords can be passed to the underlying R function via
        # exploding the dictionary
        kwargs = {
            "Data": self.r_df_,
            "var_path": self.r_model_params_["path_feature"],
            "var_conv": self.r_model_params_["conversion_feature"],
            "var_value":
                self.r_model_params_["conversion_value_feature"],
            "sep": self.r_model_params_["separator"]
        }

        # fit the model
        model = RChannelAttribution.heuristic_models(**kwargs)

        # the conversion to a pandas.DataFrame can happen here since
        # there are not multiple items returned with this function
        model = pandas2ri.ri2py(model)

        # adjust the feature names; the default names are returned by
        # the underlying c++ code via the ChannelAttribution library

        features_to_rename = {
            "channel_name": "channel name",
            "first_touch": "first touch",
            "first_touch_value": "first touch value",
            "last_touch": "last touch",
            "last_touch_value": "last touch value",
            "linear_touch": "linear touch",
            "linear_touch_value": "linear touch value"
        }

        # we'll pop the item from the dict according to the flags set
        # during instantiation
        if self.first_touch is False:
            _ = features_to_rename.pop("first_touch_conversions")
            _ = features_to_rename.pop("first_touch_value")
        if self.last_touch is False:
            _ = features_to_rename.pop("last_touch_conversions")
            _ = features_to_rename.pop("last_touch_value")
        if self.linear_touch is False:
            _ = features_to_rename.pop("linear_touch_conversions")
            _ = features_to_rename.pop("linear_touch_value")

        # apply the renaming
        model = model.rename(
            columns=features_to_rename
        )

        if self.conversion_value_feature is not None:
            _ = features_to_rename.pop("first_touch_value")
            _ = features_to_rename.pop("last_touch_value")
            _ = features_to_rename.pop("linear_touch_value")

        return model

    def _markov_model(self, r_package=None):
        """Creates the hidden markov models."""
        # get a ref to the R package so we can call the function
        RChannelAttribution = r_package

        # keywords can be passed to the underlying R function via
        # exploding the dictionary
        kwargs = {
            "Data": self.r_df_,
            "var_path": self.r_model_params_["path_feature"],
            "var_conv": self.r_model_params_["conversion_feature"],
            "var_value":
                self.r_model_params_["conversion_value_feature"],
            "var_null": self.r_model_params_["null_path_feature"],
            "order": self.r_model_params_["order"],
            "nsim": self.r_model_params_["n_simulations"],
            "max_step": self.r_model_params_["max_step"],
            "out_more": self.r_model_params_["return_transition_probs"],
            "sep": self.r_model_params_["separator"],
            "seed": self.r_model_params_["random_state"]
        }

        # fit the model
        model = RChannelAttribution.markov_model(**kwargs)

        # we're only returning a dataframe so we can make the
        # conversion back to pandas and change the feature name
        if self.return_transition_probs is False:
            model = pandas2ri.ri2py(model)
            model = model.rename(
                columns={
                    "total_conversions": "markov model",
                    "channel_name": "channel name"
                }
            )
            if self.conversion_value_feature is not None:
                model = model.rename(
                    columns={
                        "total_conversion_value": "markov value",
                        "channel_name": "channel name"
                    }
                )

        return model




