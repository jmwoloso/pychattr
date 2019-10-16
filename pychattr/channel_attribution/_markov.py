"""
Contains the model-fitting logic used for the Markov model.
"""
# Author: Jason Wolosonovich <jason@refinerynet.com>
# License: BSD 3-clause

import math
import collections

import numpy as np
import pandas as pd


class Fx(object):
    """Transition Matrix."""

    def __init__(self, nrows, ncols):

        # TODO: use scipy sparse matrices
        self.S = np.zeros((nrows, ncols), dtype=int)
        self.S0 = np.zeros((nrows, ncols), dtype=int)
        self.S1 = np.zeros((nrows, ncols), dtype=int)
        self.lrS0 = np.zeros((nrows,), dtype=int)
        self.lrS = np.zeros((nrows,), dtype=int)
        self.non_zeros = 0
        self.nrows = nrows
        self.ncols = ncols

    def add(self, ichannel_old, ichannel, vxi):
        val0 = int(self.S[ichannel_old, ichannel])
        if val0 == 0:
            lval0 = self.lrS0[ichannel_old]
            self.S0[ichannel_old, lval0] = ichannel
            self.lrS0[ichannel_old] = lval0 + 1
            self.non_zeros += 1
        self.S[ichannel_old, ichannel] = val0 + vxi
        return self

    def cum(self):
        for i in range(self.nrows):
            lrs0i = self.lrS0[i]

            if lrs0i > 0:
                self.S1[i, 0] = self.S[i, self.S0[i, 0]]
                j = 1
                while j < lrs0i:
                    self.S1[i, j] = self.S1[i, j - 1] + \
                                    self.S[i, self.S0[i, j]]

                    j += 1
                self.lrS[i] = self.S1[i, lrs0i - 1]
        return self

    def sim(self, c, uni):
        s0 = math.floor(uni * self.lrS[c] + 1)
        for k in range(self.lrS0[c]):
            if self.S1[c, k] >= s0:
                return int(self.S0[c, k])
        return 0

    def tran_matx(self, vchannels):
        vsm = []
        vk = []
        channel_from = []
        channel_to = []
        num_transitions = []
        k = 0
        for i in range(self.nrows):
            sm3 = 0
            # j = 0
            for j in range(self.lrS0[i]):
                mij = self.S[i, int(self.S0[i, j])]
                if mij > 0:
                    channel_from.append(vchannels[i])
                    channel_to.append(vchannels[int(self.S0[i, j])])
                    num_transitions.append(mij)
                    sm3 += mij
                    k += 1
            vsm.append(sm3)
            vk.append(k)

        num_transitions = np.asarray(num_transitions, dtype=float)
        vsm = np.asarray(vsm)
        vk = np.asarray(vk)

        w = 0

        for k in range(self.non_zeros):
            if k == vk[w]:
                w += 1
            num_transitions[k] /= vsm[w]

        trans_probs = num_transitions
        tmat_data = {
            "channel_from": channel_from,
            "channel_to": channel_to,
            "transition_probability": trans_probs
        }
        return pd.DataFrame(tmat_data)


def fit_markov(df, paths, convs, conv_val, nulls, nsim, max_step,
               out_more, sep, order, random_state, loops):
    var_path = df.loc[:, paths].values.tolist()
    conv = df.loc[:, convs].values.tolist()
    if conv_val:
        var_value = df.loc[:, conv_val].values.tolist()
    else:
        var_value = []
    if nulls:
        var_null = df.loc[:, nulls].values.tolist()
    else:
        var_null = []

    if random_state:
        np.random.seed(random_state)

    # do we have revenues?
    flg_var_value = True if len(var_value) > 0 else False

    # do we have nulls?
    flg_var_null = True if len(var_null) > 0 else False

    # do we allow loops?
    flg_equal = loops

    # get the list of paths
    vy = var_path

    # get the list of conversions
    vc = conv

    if flg_var_value:
        vv = var_value

    if flg_var_null:
        vn = var_null

    # how many paths do we have?
    lvy = len(vy)
    l_vui = 0
    mp_vui = collections.defaultdict(int)
    v_vui = []
    vui = 0.0
    rchannels = []
    lrchannels = j0 = z = 0
    channel_j = ""

    vchannels_sim_id = [0] * order
    mp_channels_sim_id = {}

    nchannels = 0
    nchannels_sim = 0

    vy2 = []

    mp_channels = collections.defaultdict(int)
    mp_channels_sim = {}
    mp_npassi = {}
    vnpassi = []

    mp_channels["(start)"] = 0
    vchannels = []
    vchannels.append("(start)")
    nchannels += 1

    vchannels_sim = []

    ##### BEGIN PROGRAM
    # ####################################################
    ########################################################################
    ########################################################################
    for z in range(order):
        vchannels_sim_id[z] = -1

    if order > 1:
        mp_channels_sim["(start)"] = nchannels_sim
        vchannels_sim.append("(start)")
        vchannels_sim_id[0] = nchannels_sim
        mp_channels_sim_id[nchannels_sim] = vchannels_sim_id.copy()
        nchannels_sim += 1

    if flg_var_value:
        i = 0
        for i in range(lvy):
            if vc[i] > 0:
                vui = vv[i] / vc[i]
                if vui not in list(mp_vui.keys()):
                    mp_vui[vui] = l_vui
                    v_vui.append(vui)
                    l_vui += 1
            i = i + 1

    for i in range(lvy):
        s = vy[i]

        s += sep[0]
        ssize = len(s)
        channel = ""
        path = ""
        j = 0
        npassi = 0
        rchannels = []

        while j < ssize:
            cfirst = 1
            while s[j] != sep[0]:
                if cfirst == 0:
                    if s[j] != " ":
                        end_pos = j
                elif cfirst == 1 and s[j] != " ":
                    cfirst = 0
                    start_pos = j
                    end_pos = j
                j += 1

            if cfirst == 0:
                channel = s[start_pos:end_pos+1]

                if channel not in mp_channels.keys():
                    mp_channels[channel] = nchannels
                    vchannels.append(channel)
                    nchannels += 1

                if order == 1:
                    if npassi == 0:
                        path = "0 "
                    else:
                        path += " "
                    path = path + str(mp_channels[channel])
                    npassi += 1
                else:
                    rchannels.append(channel)
            channel = ""
            j += 1

        if order > 1:
            lrchannels = len(rchannels)
            for z in range(order):
                vchannels_sim_id[z] = -1

            if lrchannels > (order - 1):
                npassi = lrchannels - order + 1

                for k in range(npassi):
                    channel = ""
                    channel_j = ""
                    z = 0
                    j0 = k + order

                    for j in range(k, j0):
                        channel_j = rchannels[j]
                        channel += channel_j
                        vchannels_sim_id[z] = mp_channels[channel_j]
                        z += 1

                        if j < (j0 - 1):
                            channel += ","

                    if channel not in list(mp_channels_sim.keys()):
                        mp_channels_sim[channel] = nchannels_sim
                        vchannels_sim.append(channel)

                        mp_channels_sim_id[nchannels_sim] = \
                            vchannels_sim_id.copy()
                        nchannels_sim += 1

                    path += str(mp_channels_sim[channel])
                    path += " "

            else:
                npassi = 1
                channel = ""
                channel_j = ""
                for j in range(lrchannels):
                    channel_j = rchannels[j]
                    channel += channel_j
                    vchannels_sim_id[j] = mp_channels[channel_j]
                    if j < (lrchannels - 1):
                        channel += ","

                if channel not in list(mp_channels_sim.keys()):
                    mp_channels_sim[channel] = nchannels_sim
                    vchannels_sim.append(channel)
                    mp_channels_sim_id[nchannels_sim] = \
                        vchannels_sim_id.copy()
                    nchannels_sim += 1
                path += str(mp_channels_sim[channel])
                path += " "
            path = "0 " + path
        else:  # end order > 1
            path += " "
        vy2.append(path + "e")
        npassi += 1

    mp_channels["(conversion)"] = nchannels
    nchannels += 1
    vchannels.append("(conversion)")

    mp_channels["(null)"] = nchannels
    nchannels += 1
    vchannels.append("(null)")

    if order > 1:
        mp_channels_sim["(conversion)"] = nchannels_sim
        vchannels_sim.append("(conversion)")
        for z in range(order):
            vchannels_sim_id[0] = nchannels_sim
        mp_channels_sim_id[nchannels_sim] = vchannels_sim_id.copy()
        nchannels_sim += 1

        mp_channels_sim["(null)"] = nchannels_sim
        vchannels_sim.append("(null)")
        for z in range(order):
            vchannels_sim_id[0] = nchannels_sim

        mp_channels_sim_id[nchannels_sim] = vchannels_sim_id.copy()
        nchannels_sim += 1

    if order == 1:
        nchannels_sim = nchannels

    npassi = 0

    S = Fx(nchannels_sim, nchannels_sim)
    fV = Fx(nchannels_sim, l_vui)

    for i in range(lvy):
        s = vy2[i]
        s += " "
        ssize = len(s)

        channel = ""
        channel_old = ""
        ichannel_old = 0
        ichannel = 0

        j = 0
        npassi = 0

        vci = vc[i]

        if flg_var_null:
            vni = vn[i]
        else:
            vni = 0
        vpi = vci + vni

        while j < ssize:
            start_j = j
            while s[j] != " ":
                if j < ssize:
                    channel = s[start_j:(j+1)]
                j = j + 1
                continue
            j = j + 1

            if flg_equal or channel != channel_old:
                if channel[0] != "0":
                    if channel[0] == "e":
                        npassi += 1
                        if vci > 0:
                            ichannel = nchannels_sim - 2
                            S.add(ichannel_old, ichannel, vci)
                            if flg_var_value:
                                vui = vv[i] / vci
                                fV.add(ichannel_old, mp_vui[vui], vci)
                            if vni > 0:
                                ichannel = nchannels_sim - 1
                                S.add(ichannel_old, ichannel, vni)
                                continue
                            else:
                                continue
                        if vni > 0:
                            ichannel = nchannels_sim - 1
                            S.add(ichannel_old, ichannel, vni)
                        else:
                            continue
                    else:
                        if vpi > 0:
                            ichannel = int(channel)
                            S.add(ichannel_old, ichannel, vpi)
                    npassi += 1
                else:
                    ichannel = 0
                channel_old = channel
                ichannel_old = ichannel
            continue

        channel = ""
        j = j + 1

    if out_more:
        if order == 1:
            trans_mat = S.tran_matx(vchannels)
        else:
            trans_mat = S.tran_matx(vchannels_sim)

    S = S.cum()

    nuf = int(1e6)
    nconv = 0
    sval0 = 0
    ssval = 0
    c_last = 0
    iu = 0
    vunif = np.random.uniform(size=nuf)

    C = [0] * nchannels
    T = [0] * nchannels
    V = [0] * nchannels

    if flg_var_value:
        fV.cum()

    if max_step == 0:
        max_npassi = nchannels_sim * 10
    else:
        max_npassi = int(1e6)

    if nsim == 0:
        nsim = int(1e6)

    for i in range(nsim):
        c = 0
        npassi = 0
        for k in range(nchannels):
            C[k] = 0

        C[c] = 1
        while npassi <= max_npassi:
            if iu >= nuf:
                vunif = np.random.uniform(size=nuf)
                iu = 0
            c = S.sim(c, vunif[iu])
            iu += 1

            if c == (nchannels_sim - 2):
                break
            elif c == (nchannels_sim - 1):
                break
            if order == 1:
                C[c] = 1

            else:
                for k in range(order):
                    id0 = mp_channels_sim_id[c][k]
                    if id0 >= 0:
                        C[id0] = 1
                    else:
                        break
            c_last = c
            npassi = npassi + 1

        if c == (nchannels_sim - 2):
            nconv += 1

            if flg_var_value:
                if iu >= nuf:
                    vunif = np.random.uniform(size=nuf)
                    iu = 0
                sval0 = v_vui[fV.sim(c_last, vunif[iu])]
                iu += 1
            ssval = ssval + sval0

            for k in range(nchannels):
                if C[k] == 1:
                    T[k] = T[k] + 1
                    if flg_var_value:
                        V[k] = V[k] + sval0

    T[0] = 0
    nch0 = nchannels - 3
    T[nchannels - 2] = 0
    T[nchannels - 1] = 0

    sn = 0

    for i in range(lvy):
        sn = sn + vc[i]

    sm = 0

    for i in range(nchannels - 1):
        sm = sm + T[i]

    TV = [0] * nch0
    rTV = [0] * (nch0)

    for k in range(nch0 + 1):
        if sm > 0:
            TV[k - 1] = (T[k] / sm) * sn
            if out_more:
                # removal effects
                rTV[k - 1] = T[k] / nconv

    VV = [0] * nch0

    rVV = [0] * nch0

    if flg_var_value:
        V[0] = 0
        V[nchannels - 2] = 0
        V[nchannels - 1] = 0

        sn = 0
        for i in range(lvy):
            sn = sn + vv[i]

        sm = 0
        for i in range(nchannels - 1):
            sm = sm + V[i]

        for k in range(nch0 + 1):
            if sm > 0:
                VV[k - 1] = (V[k] / sm) * sn
                if out_more:
                    # removal effects
                    rVV[k - 1] = V[k] / ssval

    vchannels0 = list(range(nch0))

    for k in range(nch0 + 1):
        vchannels0[k - 1] = vchannels[k]

    if flg_var_value:
        if not out_more:
            df = pd.DataFrame(
                {
                    "channel_name": vchannels0,
                    "total_conversions": TV,
                    "total_revenue": VV
                }
            )
            return df
        else:
            df = pd.DataFrame({
                "channel_name": vchannels0,
                "total_conversions": TV,
                "total_revenue": VV
            })

            re_df = pd.DataFrame({
                "channel_name": vchannels0,
                "removal_effect": rTV,
                "removal_effect_value": rVV
            })

            tmat = trans_mat.copy()
            return df, re_df, tmat
    else:
        if not out_more:
            df = pd.DataFrame({
                "channel_name": vchannels0,
                "total_conversions": TV
            })
            return df
        else:
            df = pd.DataFrame({
                "channel_name": vchannels0,
                "total_conversions": TV
            })

            re_df = pd.DataFrame({
                "channel_name": vchannels0,
                "removal_effect": rTV
            })

            tmat = trans_mat.copy()
            return df, re_df, tmat
