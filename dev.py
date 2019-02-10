import pandas as pd
import collections






class PyChAttr(object):
    def __init__(self, df=None, markov_model=True, heuristic_model=True,
                 first_touch=True, last_touch=True,
                 linear_touch=True, path_feature=None,
                 conversion_feature=None, conversion_value_feature=None,
                 null_path_feature=None, separator=">", order=1,
                 n_simulations=None, max_step=None,
                 return_transition_probs=True, random_state=None,
                 return_plot_data=True):
        pass

    def fit(self):
        pass

    def predict(self):
        pass











def _heuristic_models(df=None, path_feature=None,
                      conversion_feature=None,
                      conversion_value_feature=None,
                      separator=">"):
    """Creates the heuristic models."""
    # whether we have conversion values that need calculated as well
    has_values = False if conversion_value_feature is None else True
    # grab the values
    if has_values is True:
        vv = df.loc[:, conversion_value_feature].values

    # grab the paths
    vy = df.loc[:, path_feature].values
    # this needs to be an array of arrays of strings
    vy = [path.split(" > ") for path in vy]
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
    print("lvy")
    for i in range(lvy):
        s = vy[i]
        # s += " " + sep
        ssize = len(s)
        channel = ""
        j = 0
        nchannels_unique = 0

        n_path_length = 0
        print("while1")
        while j < ssize:
            cfirst = 1
            print("while2")
            while s[j] != sep:
                print(s[j])
                if cfirst == 0:
                    if s[j] != " ":
                        end_pos = j
                    elif cfirst == 1 & s[j] != " ":
                        cfirst = 0
                        start_pos = j
                        end_pos = j
            j += 1
            print(j)

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
        mp_last_conv[channel_last] = mp_last_conv[channel_last] + \
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
            mp_last_val[channel_last] = mp_last_val[channel_last] \
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
    print("nchannels")
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


df = pd.read_csv("/home/jason/source_code/python_packages/pychattr"
                 "/demo_data_small.csv",
                 header=0)

output = _heuristic_models(df=df,
                           path_feature="path",
                           conversion_feature="total_conversions",
                           conversion_value_feature="total_conversion_value",
                           )
