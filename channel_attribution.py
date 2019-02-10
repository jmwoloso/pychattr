import collections
import numpy as np
import pandas as pd




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
            heuristic = \
              self._heuristic_models(
                  df=self.df,
                  path_feature=self.path_feature,
                  conversion_feature=self.conversion_feature,
                  conversion_value_feature=self
                      .conversion_value_feature,
                  separator=self.separator
              )
            self.heuristic_ = heuristic.copy()

            # markov
            markov = self._markov_model(df=self.df)

            if self.return_transition_probs is True:
                self.transition_matrix_ = markov[1]
                self.removal_effects_ = markov[2]
                markov = markov[0]

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
                self._heuristic_models(
                    df=self.df,
                    path_feature=self.path_feature,
                    conversion_feature=self.conversion_feature,
                    conversion_value_feature=self
                        .conversion_value_feature,
                    separator=self.separator
                )

        # fit markov only
        elif self.markov_model is True and self.heuristic_model is \
                False:
            markov = self._markov_model(df=self.df)

            if self.return_transition_probs is True:
                self.transition_matrix_ = markov[1]
                self.removal_effects_ = markov[2]
                markov = markov[0]
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


    def _heuristic_models(self,df=None, path_feature=None,
                          conversion_feature=None,
                          conversion_value_feature=None,
                          separator=">>"):
        """Creates the heuristic models."""
        # whether we have conversion values that need calculated as well
        has_values=False if conversion_value_feature is None else True
        # grab the values
        if has_values is True:
            vv = df.loc[:, conversion_value_feature].values

        # grab the paths
        vy = df.loc[:, path_feature].values
        lvy = len(vy)

        # grab the conversions
        vc = df.loc[:, conversion_feature].values

        sep = separator

        nchannels = 0
        mp_channels = collections.OrderedDict()
        vchannels = list()
        mp_first_conv = collections.OrderedDict()
        mp_first_val = collections.OrderedDict()
        mp_last_conv = collections.OrderedDict()
        mp_last_val = collections.OrderedDict()
        mp_linear_conv = collections.OrderedDict()
        mp_linear_val = collections.OrderedDict()
        mp0_linear_conv = collections.OrderedDict()
        mp0_linear_val = collections.OrderedDict()
        vchannels_unique = list()


        for i in range(lvy):
            s = vy[i]
            s+= sep
            ssize = len(s)
            channel = ""
            j = 0
            nchannels_unique = 0

            n_path_length = 0

            while j < ssize:
                cfirst = 1
                while s[j]!= sep:
                    if cfirst == 0:
                        if s[j] != " ":
                            end_pos=j
                        elif cfirst == 1 & s[j] != " ":
                            cfirst = 0
                            start_pos = j
                            end_pos = j
                    j += 1

                if cfirst == 0:
                    channel = s[start_pos:end_pos - start_pos + 1]

                    if mp_channels[channel] == \
                        list(mp_channels.keys())[-1]:
                        mp_channels[channel] = nchannels
                        vchannels.append(channel)
                        nchannels += 1

                        mp_first_conv[channel] = 0
                        mp_last_conv[channel] = 0
                        mp_linear_conv[channel] = 0
                        mp0_linear_conv[channel] = 0

                        if has_values is True:
                            mp_first_val[channel] = 0
                            mp_last_val[channel] = 0
                            mp_linear_val[channel] = 0
                            mp0_linear_val[channel] = 0

                    if nchannels_unique == 0:
                        vchannels.append(channel)
                        nchannels_unique += 1
                    elif channel in vchannels_unique and channel == \
                            vchannels_unique[-1]:
                        vchannels_unique.append(channel)
                        nchannels_unique += 1

                    mp0_linear_conv[channel] = mp0_linear_conv[
                                                   channel] + vc[i]
                    if has_values is True:
                        mp0_linear_val[channel] = mp0_linear_val[
                            channel] + vv[i]
                    n_path_length += 1

                    channel_last = channel

                channel = ""
                j += 1

            channel_first = vchannels_unique[0]
            mp_first_conv[channel_first] = mp_first_conv[
                                               channel_first] + vc[i]
            mp_last_conv[channel_last] = mp_last_conv[channel_last] +\
                                         vc[i]

            k = 0
            for k in range(nchannels_unique):
                kchannel = vchannels_unique[k]
                mp_linear_conv[kchannel] = mp_linear_conv[kchannel] + (
                    mp0_linear_conv[kchannel] / n_path_length
                )
            if has_values is True:
                mp_first_val[channel_first] = mp_first_val[
                    channel_first] + vv[i]
                mp_last_val[channel_last] = mp_last_val[channel_last]\
                                            + vv[i]
                k = 0
                for k in range(nchannels_unique):
                    kchannel = vchannels_unique[k]
                    mp_linear_val[kchannel] = \
                        mp_linear_val[kchannel] + (
                            mp0_linear_val[kchannel] / n_path_length
                        )
        vfirst_conv = [nchannels]
        vlast_conv = [nchannels]
        vlinear_conv = [nchannels]

        vfirst_val = [nchannels]
        vlast_val = [nchannels]
        vlinear_val = [nchannels]

        k = 0
        for k in range(nchannels):
            kchannel = vchannels[k]
            vfirst_conv[k] = mp_first_conv[kchannel]
            vlast_conv[k] = mp_last_conv[kchannel]
            vlinear_conv[k] = mp_linear_conv[kchannel]

            if has_values is True:
                vfirst_val[k] = mp_first_val[kchannel]
                vlast_val[k] = mp_last_val[kchannel]
                vlinear_val[k] = mp_linear_val[kchannel]

        if has_values is True:
            output = collections.OrderedDict()
            output["channel_name"] = vchannels
            output["first_touch_conversions"] = vfirst_conv
            output["first_touch_value"] = vfirst_val
            output["last_touch_conversions"] = vlast_conv
            output["last_touch_value"] = vlast_val
            output["linear_touch_conversions"] = vlinear_conv
            output["linear_touch_value"] = vlinear_val
        else:
            output = collections.OrderedDict()
            output["channel_name"] = vchannels
            output["first_touch_conversions"] = vfirst_conv
            output["last_touch_conversions"] = vlast_conv
            output["linear_touch_conversions"] = vlinear_conv
        return output




        return

    def _markov_model(self, df=None):
        """Creates the hidden markov models."""

        return

