"""
Contains the model-fitting logic used for the Markov model.
"""
# Author: Jason Wolosonovich <jason@avaland.io>
# License: BSD 3-clause
import itertools
import math
import collections

import numpy as np
import pandas as pd


class Fx(object):
    """Transition Matrix."""
    def __init__(self, ncols, nrows):

        # TODO: use scipy sparse matrices
        self.S = np.zeros((ncols, nrows), dtype=int)
        self.S0 = np.zeros((ncols, nrows), dtype=int)
        self.S1 = np.zeros((ncols, nrows), dtype=int)
        self.lrS0 = np.zeros((nrows, ), dtype=int)
        self.lrS = np.zeros((nrows,), dtype=int)
        self.non_zeros = 0
        self.nrows = nrows
        self.ncols = ncols


    def add(self, ichannel_old, ichannel, vxi):
        val0 = int(self.S[ichannel_old, ichannel])
        # print(f"vxi: {vxi}")
        # print(f"ichannel_old: {ichannel_old}")
        # print(f"ichannel: {ichannel}")
        # print(f"val0: {val0}")
        if val0 == 0:
            lval0 = self.lrS0[ichannel_old]
            # print(f"lval0: {lval0}")
            self.S0[ichannel_old, lval0] = ichannel
            # print(f"S0[ichannel_old, lval0]: {self.S0[ichannel_old, lval0]}")
            self.lrS0[ichannel_old] = lval0 + 1
            # print(f"lrS0[ichannel_old]: {self.lrS0[ichannel_old]}")
            self.non_zeros += 1

        self.S[ichannel_old, ichannel] = val0 + vxi
        # print(f"S[ichannel_old, ichannel]: {self.S[ichannel_old, ichannel]}")
        return self

    def cum(self):
        for i in range(self.nrows):
            # lrs0i = self.lrS0[i]

            # i = 0
            # while i < self.nrows:
            # while i < self.nrows:
            #     print(f"i: {i}")
            lrs0i = self.lrS0[i]
            # print(f"lrs0i: {lrs0i}")
            if lrs0i > 0:
                # s0 = self.S0[i, 0]
                # print(f"s0: {s0}")
                # print(f"S(i, s0): {self.S[i, s0]}")
                # self.S1[i, 0] = self.S[i, s0]
                # print(f"S: \n{self.S}")
                self.S1[i, 0] = self.S[i, self.S0[i, 0]]
                # print(f"S0: \n {self.S0}")
                # print(f"S1: \n {self.S1}")
                # print(f"S1(i, 0): {self.S1[i, 0]}")
                # print(f"S: \n {self.S}")
                # print(f"S(i, S0(i, 0)): \n {self.S[i, self.S0[i, 0]]}")
                # print(f"S1(i, 0): {self.S1[i, 0]}")
                # print(f"S: \n {self.S}")
                # print(f"S0: \n {self.S0}")
                # print(f"S1: \n {self.S1}")

                # print(f"S0(i, 0): {self.S0[i, 0]}")
                # print(f"i (again): {i}")
                j = 1
                while j < lrs0i:
                    self.S1[i, j] = self.S1[i, j - 1] + \
                                    self.S[i, self.S0[i, j]]
                    # print(f"S1(i, j): {self.S1[i, j]}")
                    j += 1
                self.lrS[i] = self.S1[i, lrs0i - 1]
                # print(f"lrS[i]: {self.lrS[i]}")
            # i = i + 1
        return self


    def sim(self, c, uni):
        s0 = math.floor(uni * self.lrS[c] + 1)
        # print(f"s0: {s0}")
        # k = 0
        # while k < self.lrS0[c]:
        for k in range(self.lrS0[c]):
            # print(f"k: {k}")
            # print(f"lrS0[c]: {self.lrS0[c]}")
            # for k in range(self.lrS0[c]):
            if self.S1[c, k] >= s0:
                # print("returning from if condition")
                return int(self.S0[c, k])
        # print("returning from outer loop")
        return 0
        # k = k + 1
        # return val
        # val = int(self.S0[c, k])
        # else:
        #     val = int(0)
        # k = k + 1
        # yield val

    def tran_matx(self,vchannels):
        vsm = []
        vk = []
        vM1 = []
        vM2 = []
        vM3 = []
        k = 0
        i = 0
        while i < self.nrows:
            sm3 = 0
            j = 0
            while j < self.lrS0[i]:
                mij = self.S[i, int(self.S0[i, j])]
                # print(f"mij: {mij}")
                if mij > 0:
                    vM1.append(vchannels[i])
                    # print(f"vM1[k]: {vM1[k]}")
                    vM2.append(vchannels[int(self.S0[i, j])])
                    # print(f"vM2[k]: {vM2[k]}")
                    vM3.append(mij)
                    # print(f"vM3[k]: {vM3[k]}")
                    sm3 = sm3 + mij
                    # print(f"sm3: {sm3}")
                    k = k + 1
                j = j + 1
            i = i + 1

            vsm.append(sm3)
            vk.append(k)

        vM3 = np.asarray(vM3, dtype=float)
        vsm = np.asarray(vsm)
        vk = np.asarray(vk)

        w = 0
        k = 0

        # print(f"vM3: {vM3}")
        while k < self.non_zeros:
            if k == vk[w]:
                # print("skipping iteration")
                w += 1
            # v = vM3[k] / vsm[w]
            # print(f"v: {v}")
            # vM3[k] = v
            vM3[k] /= vsm[w]
            # print(f"vsm[w]: {vsm[w]}")
            # print(f"vM3[k]: {vM3[k]}")
            k += 1
        return vM3

# def conv(c, nchannels_sim, nconv, flg_var_value, iu, nuf, v_vui)


var_path = [
    # ["A", "B", "A", "B", "B", "A"],
    # ["A", "B", "B", "A", "A"],
    # ["A", "A"],
    "A > B > A > B > B > A",
    "A > B > B > A > A",
    "A > A"
]
conv = [
    1,
    1,
    1
]
var_value = []
var_null = []
nsim = 1
max_step = 1
out_more = True
sep = ">"
order = 2
random_state=None

if random_state:
    np.random.seed(random_state)

# do we have revenues?
flg_var_value = True if len(var_value) > 0 else False


# do we have nulls?
flg_var_null = True if len(var_null) > 0 else False

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
# print(lvy)
l_vui = 0
mp_vui = collections.defaultdict(int)
v_vui = []
vui = 0.0
rchannels = []
lrchannels = j0 = z = 0
channel_j = ""

# vchannels_sim_id = [i for i in range(order)]
vchannels_sim_id = [0] * order
mp_channels_sim_id = {}

nchannels = 0
nchannels_sim = 0

# vy2 = [i for i in range(lvy)]
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



##### BEGIN PROGRAM ####################################################
########################################################################
########################################################################
for z in range(order):
    # TODO: PASSED
    vchannels_sim_id[z] = -1


# if order > 1:
#     # TODO: PASSED
#     mp_channels_sim["(start)"] = nchannels_sim
#     vchannels_sim.append("(start)")
#     vchannels_sim_id[0] = nchannels_sim
#     # print(f"vchannels_sim_id: ")
#     # for i, c in enumerate(vchannels_sim_id):
#     #     print(f"vchannels_sim_id[{i}]: {c}")
#     # print(f"nchannels_sim: {nchannels_sim}")
#     # TODO: PASSED
#     mp_channels_sim_id[nchannels_sim] = vchannels_sim_id
#     # print(vchannels_sim_id)
#     # print(mp_channels_sim_id)
#     # print(f"vchannels_sim_id: {vchannels_sim_id}")
#     # print(f"mp_channels_sim_id: {mp_channels_sim_id}")
#     # print(f"vchannels_sim_id[0]: {vchannels_sim_id[0]}")
#     # TODO: PASSED
#     # print(f"nchannels_sim: {nchannels_sim}")
#     nchannels_sim += 1
#     # print()
#     # print(f"nchannels_sim: {nchannels_sim}")
# print(f"mp_channels_sim_id: {mp_channels_sim_id}")
# TODO: NOT PASSED
# if flg_var_value:
#     i = 0
#     while i < lvy:
#         if vc[i] > 0:
#             vui = vv[i] / vc[i]
#             if mp_vui[vui] not in list(mp_vui.keys()):
#                 mp_vui[vui] = l_vui
#                 v_vui.append(vui)
#                 l_vui += 1
#         i = i + 1

# i = 0
# # while i < lvy:
# for i in range(i, lvy):
#     # print(f"i: {i}")
#     s = vy[i]
#
#     s += sep[0]
#     ssize = len(s)
#     channel = ""
#     path = ""
#     j = 0
#     npassi = 0
#     rchannels = []
    #
    # while j < ssize:
    # for j in range(ssize):
    #     # TODO: PASSED
    #     # print(f"(ssize) j:{j}")
    #     cfirst = 1
    #     # print(f"cfirst: {cfirst}")
    #     # print(f"j: {j}")
    #     while s[j] != sep[0]:
    #         # TODO: PASSED
    #         # print(f"s[j]: {s[j]}")
    #         if cfirst == 0:
    #             # TODO: PASSED
    #             # print(f"cfirst: {cfirst}")
    #             if s[j] != " ":
    #                 end_pos = j
    #         elif cfirst == 1 and s[j] != " ":
    #             #TODO: PASSED
    #             # print(f"cfirst: {cfirst}")
    #             cfirst = 0
    #             start_pos = j
    #             end_pos = j
    #         j += 1
    #
    #     if cfirst == 0:
    #         # TODO: PASSED
    #         # print(f"cfirst: {cfirst}")
    #         # print(s)
    #         # print(start_pos)
    #         # print(end_pos)
    #         channel = s[start_pos]
    #         # channel = s[start_pos]
    #         # print(f"channel: {channel}")
    #         # channel = s[start_pos: (end_pos - start_pos + 1)]
    #         # print(channel)
    #
    #         if channel not in mp_channels.keys():
    #             # TODO: PASSED
    #             # print(f"channel: {channel}")
    #             mp_channels[channel] = nchannels
    #             vchannels.append(channel)
    #             nchannels = nchannels + 1
    #
    #         if order == 1:
    #             # print(f"order: {order}")
    #             if npassi == 0:
    #                 # print(f"npassi: {npassi}")
    #                 path = "0 "
    #             else:
    #                 # print(f"npassi: {npassi}")
    #                 path += " "
    #             # path = " " + str(mp_channels[channel])
    #             path = path + str(mp_channels[channel])
    #             npassi = npassi + 1
    #             # print(f"path: {path}")
    #         else:
    #             # TODO: PASSED
    #             # print(f"rchannels.append(): {channel}")
    #             rchannels.append(channel)
    #     # channel = ""
    #     # j = j + 1
    #     # continue

    # if order > 1:
    #     # print(f"order: {order}")
    #     lrchannels = len(rchannels)
    #     # print(f"lrchannels: {lrchannels}")
    #     for z in range(order):
    #         # print(f"z: {z}")
    #         vchannels_sim_id[z] = -1
    #
    #     if lrchannels > (order - 1):
    #         # print(f"lrchannels: {lrchannels}")
    #         npassi = lrchannels - order + 1
    #         # print(f"npassi: {npassi}")
    #
    #         for k in range(npassi):
    #             # print(f"k: {k}")
    #             channel = ""
    #             channel_j = ""
    #             z = 0
    #             j0 = k + order
    #             j = k
    #             # print(f"j0: {j0}")
    #             # while j < j0:
    #             for j in range(k,j0):
    #                 # k = j
    #                 # TODO: PASSED
    #                 # print(f"z: {z}")
    #                 # print(f"i: {i}")
    #                 channel_j = rchannels[j]
    #                 print(f"channel_j: {channel_j}")
    #                 # print(f"channel: {channel}")
    #                 channel += channel_j
    #                 # print(f"channel: {channel}")
    #                 vchannels_sim_id[z] = mp_channels[channel_j]
    #                 # print(f"vchannels_sim_id[z]: {vchannels_sim_id[z]}")
    #                 # print(f"vchannels_sim_id: ")
    #                 # print(f"{vchannels_sim_id}")
    #                 # for i,c in enumerate(vchannels_sim_id):
    #                 #     print(f"vchannels_sim_id[{i}]: {c}")
    #                 z += 1
    #                 # print(f"III: {i}")
    #                 # print(f"j: {j}, j0: {j0}")
    #                 if j < (j0 - 1):
    #                     channel += ","
    #                     # print(f"channel*: {channel}")
    #                 #print(f"III: {i}")
    #             # if channel == list(mp_channels_sim.keys())[-1]:
    #             if channel not in list(mp_channels_sim.keys()):
    #                 # print(f"channel: {channel}")
    #                 mp_channels_sim[channel] = nchannels_sim
    #                 vchannels_sim.append(channel)
    #                 # for i,c in enumerate(vchannels_sim):
    #                 # print(f"vchannels_sim[{i}]: {c}")
    #                 # print(f"vchannels_sim: {vchannels_sim}")
    #                 # print(f"vchannels_sim_id: {vchannels_sim_id}")
    #                 # print(f"adding channel to mp_channels_sim_id")
    #                 # print(f"vchannels_sim_id: {vchannels_sim_id}")
    #                 # TODO: PASSED
    #                 mp_channels_sim_id[nchannels_sim] = \
    #                     vchannels_sim_id
    #                 for k, v in mp_channels_sim_id.items():
    #                     print(f"{k}: {v}")
    #                 nchannels_sim += 1
    #                 # print(nchannels_sim)
    #             # path += str(mp_channels_sim[channel])
    #             path += str(mp_channels_sim[channel])
    #             # print(f"path: {path}")
    #             path += " "
    #             # print(f"path*: {path}")
    #             # print("HERE")
    #             # end for k
    #     else:
    #         # print("HERE2")
    #         npassi = 1
    #         channel = ""
    #         channel_j = ""
    #         for j in range(lrchannels):
    #             # print(f"lrchannels: {lrchannels}")
    #             channel_j = rchannels[j]
    #             channel += channel_j
    #             vchannels_sim_id[j] = mp_channels[channel_j]
    #             # print(mp_channels[channel_j])
    #             # print("HERE3")
    #             # print(f"HERE j = {j}")
    #             if j < (lrchannels - 1):
    #                 # print("HERE4")
    #                 channel += ","
    #                 # print("HERE")
    #
    #         # if channel == list(mp_channels_sim.keys())[-1]:
    #         if channel not in list(mp_channels_sim.keys()):
    #             mp_channels_sim[channel] = nchannels_sim
    #             vchannels_sim.append(channel)
    #             # print(f"channel == last")
    #             mp_channels_sim_id[nchannels_sim] = vchannels_sim_id
    #             print(mp_channels_sim_id)
    #             nchannels_sim += 1
    #         path += str(mp_channels_sim[channel])
    #         path += " "
    #         # end else
    #         # i += 1
    #         # continue
    #     path = "0 " + path
    # else: # end order > 1
    #     path += " "
    #     # print(f"path: {path}")

    # print(path)
    vy2.append(path + "e")
    # print(vy2)
    npassi += 1
    # i = i + 1
    # TODO: PASSED
    # print(f"INCREMENTING i")
    # print()
    # print()
    # end for

# mp_channels["(conversion)"] = nchannels
# nchannels += 1
# vchannels.append("(conversion)")
#
# mp_channels["(null)"] = nchannels
# nchannels += 1
# vchannels.append("(null)")
#
# if order > 1:
#     # print(f"order: {order}")
#     mp_channels_sim["(conversion)"] = nchannels_sim
#     vchannels_sim.append("(conversion)")
#     # z = 0
#     # while z < order:
#     for z in range(order):
#         # print(f"z: {z}")
#         vchannels_sim_id[0] = nchannels_sim
#         # print(f"nchannels_sim: {nchannels_sim}")
#         # z = z + 1
#     mp_channels_sim_id[nchannels_sim] = vchannels_sim_id
#     # print(mp_channels_sim_id)
#     nchannels_sim += 1
#     # print(f"nchannels_sim*: {nchannels_sim}")
#
#     mp_channels_sim["(null)"] = nchannels_sim
#     vchannels_sim.append("(null)")
#     for z in range(order):
#         # print(f"z: {z}")
#         vchannels_sim_id[0] = nchannels_sim
#
#     mp_channels_sim_id[nchannels_sim] = vchannels_sim_id
#     nchannels_sim += 1
#
# if order == 1:
#     nchannels_sim = nchannels
#     # print(f"nchannels_sim: {nchannels_sim}")
#
# npassi = 0
#
# S = Fx(nchannels_sim, nchannels_sim)
# fV = Fx(nchannels_sim, l_vui)
# #
# # i = 0
# for i in range(lvy):
#     # print(i)
#     # print(i)
#     s = vy2[i]
#     # print(f"s: {s}")
#     s += " "
#     # print(f"s: {s}")
#     ssize = len(s)
#
#     channel = ""
#     # print(channel)
#     channel_old = ""
#     ichannel_old = 0
#     ichannel = 0
#
#     j = 0
#     npassi = 0
#
#     vci = vc[i]
#     # print(f"vci: {vci}")
#
#     if flg_var_null:
#         vni = vn[i]
#     else:
#         vni = 0
#     vpi = vci + vni
#     # print(f"vpi: {vpi}")
#
#     # print(ssize)
#     # print(s)
#
#     while j < ssize:
#         # print("while j < ssize")
#         while s[j] != " ":
#             # print("while s[j] != ' ' ")
#             if j < ssize:
#                 channel = s[j]
#                 # print(f"channel: {channel}")
#                 # print("inside")
#                 # j = j + 1
#             # print("increment j")
#             j = j + 1
#             # print(f"j: {j}")
#             # break
#             continue
#         # print("outside")
#         # print("about to restart")
#
#         # print(f"j: {j}")
#         # continue
#         j = j + 1
#
#         if channel != channel_old:
#             # print("if channel.compare")
#             if channel[0] != "0":
#                 # print("channel[0] != '0'")
#                 if channel[0] == "e":
#                     # print("channel[0] == 'e'")
#                     # print(vci)
#                     npassi += 1
#                     if vci > 0:
#                         ichannel = nchannels_sim - 2
#                         S.add(ichannel_old, ichannel, vci)
#                         if flg_var_value:
#                             vui = vv[i] / vci
#                             # print(mp_vui)
#                             fV.add(ichannel_old, mp_vui[vui], vci)
#                         if vni > 0:
#                             ichannel = nchannels_sim - 1
#                             S.add(ichannel_old, ichannel, vni)
#                             continue
#                         else:
#                             continue
#                     if vni > 0:
#                         ichannel = nchannels_sim - 1
#                         S.add(ichannel_old, ichannel, vni)
#                     else:
#                         continue
#                 else:
#                     if vpi > 0:
#                         ichannel = int(channel)
#                         S.add(ichannel_old, ichannel, vpi)
#                 npassi += 1
#             else:
#                 ichannel = 0
#             channel_old = channel
#             ichannel_old = ichannel
#             # print(f"channel_old: {channel_old}")
#             # print(f"ichannel_old: {ichannel_old}")
#         # continue
#     # print("outside")
#
#     # channel = ""
#     # j = j + 1
#     # print("about to restart")
#     # print(f"j: {j}")
#     # i = i + 1
#     # print("continuing")
#
#
#
# if out_more:
#     if order == 1:
#         trans_mat = S.tran_matx(vchannels)
#         # print(trans_mat)
#     else:
#         trans_mat = S.tran_matx(vchannels_sim)
#
#
# S = S.cum()
#
# nuf = int(1e6)
# nconv = 0
# sval0 = 0
# ssval = 0
# c_last = 0
# iu = 0
# vunif = np.random.uniform(size=nuf)
# vunif = [
#     0.0165923,
#     0.289478,
#     0.874494,
#     0.799922
# ]
#
# # C = [0] * nchannels
# T = [0] * nchannels
# V = [0] * nchannels
# C = []
# # T = []
# # V = []
#
#
#
# if flg_var_value:
#     fV.cum()
#
# if max_step == 0:
#     # max_npassi = 10
#     max_npassi = nchannels_sim * 10
#     # print(f"max_npassi: {max_npassi}")
# else:
#     # TODO: put this back in place
#     max_npassi = int(1e6)
#     # print(f"max_npassi: {max_npassi}")
#     # max_npassi = max_step
#
# if nsim == 0:
#     nsim = int(1e6)
#
# # for i in range(nsim):
# # for i in range(nsim):
# # i = 0
# for i in range(nsim):
#     # print(i)
#     c = 0
#     npassi = 0
#     # kk = 0
#     for k in range(nchannels):
#         # while kk < nchannels:
#         # C[k] = 0
#         C.append(0)
#         # print(f"k: {k}")
#         # print(f"C[k]: {C[k]}")
#         # kk = kk + 1
#
#     C[c] = 1
#     while npassi <= max_npassi:
#         # print(f"npassi: {npassi}")
#         # print(f"max_npassi: {max_npassi}")
#         # print(f"{npassi}: {max_npassi}")
#         if iu >= nuf:
#             vunif = np.random.uniform(size=nuf)
#             iu = 0
#             # print(npassi)
#         # print(iu)
#         # print(iu)
#         # print(f"vunif[iu]: {vunif[iu]}")
#         c = S.sim(c, vunif[iu])
#         # print(f"c (after sim): {c}")
#         # print(c)
#         iu += 1
#
#         if c == (nchannels_sim - 2):
#             # npassi = max_npassi + 1
#             # continue
#             # print("goto conv triggered")
#             break
#             # nconv
#             # nconv = go_to_conv(nconv)
#             # break
#             # nconv = nconv + 1
#             #
#             # if flg_var_value:
#             #     if iu > nuf:
#             #         vunif = np.random.uniform(size=nuf)
#             #         iu = 0
#             #     sval0 = v_vui.append(
#             #         fV.sim(c_last, vunif[iu]))
#             #     iu += 1
#             # ssval = ssval + sval0
#             # # print(f"ssval: {ssval}")
#             #
#             # for k in range(nchannels):
#             #     if C[k] == 1:
#             #         T[k] = T[k] + 1
#             #         if flg_var_value:
#             #             V[k] = V[k] + sval0
#             # continue
#             # kk = kk + 1
#             # npassi = npassi + 1
#             # print(f"goto conv triggered")
#             # break
#         elif c == (nchannels_sim - 1):
#             # pass
#             # continue
#             # print(f"goto null triggered")
#             # break
#             # npassi = max_npassi + 1
#             # print("goto null triggered")
#             break
#         if order == 1:
#             C[c] = 1
#
#         else:
#             # for k,v in mp_channels_sim_id.items():
#             #     print(f"{k}: {v}")
#             for k in range(order):
#                 # print(f"k: {k}")
#                 # print(f"order: {order}")
#                 # print(f"c: {c}")
#                 # print(f"mp_channels_sim_id: {mp_channels_sim_id}")
#                 id0 = mp_channels_sim_id[c][k]
#                 # print(f"id0:{id0}")
#                 # print(f"C: {C}")
#                 # print(f"mp_channels_sim_id: {mp_channels_sim_id}")
#                 # print(f"mp_channels_sim_id: {mp_channels_sim_id}")
#                 # print(f"id0: {id0}")
#                 # print(f"mp_channels_sim_id: {mp_channels_sim_id}")
#                 if id0 >= 0:
#                     # print(f"id0: {id0}")
#                     C[id0] = 1
#                 else:
#                     break
#                 # kk = kk + 1
#         c_last = c
#         # print(f"c_last: {c_last}")
#         npassi = npassi + 1
#         # continue
#
#     if c == (nchannels_sim - 2):
#         # print("go_to_conv")
#         nconv += 1
#
#         if flg_var_value:
#             if iu > nuf:
#                 vunif = np.random.uniform(size=nuf)
#                 iu = 0
#             # sval0 = v_vui.append(list(fV.sim(c_last, vunif[iu]))[0])
#             sval0 = v_vui.append(fV.sim(c_last, vunif[iu]))
#             iu += 1
#         ssval = ssval + sval0
#
#         # kk = 0
#         for k in range(nchannels):
#             # print(f"k: {k}")
#             # print(f"nchannels: {nchannels}")
#             # print(f"C[k]: {C[k]}")
#             if C[k] == 1:
#                 T[k] = T[k] + 1
#                 # print(f"T[k]: {T[k]}")
#                 if flg_var_value:
#                     V[k] = V[k] + sval0
#         # continue
#     # print("go_to_null")
#     # if c == (nchannels_sim - 1):
#     #     print("go_to_null")
#     # continue
#     # continue
#     # kk = kk + 1
#     # i = i + 1
#     # continue
# # print("exiting")
# T[0] = 0
# # print(f"T[0]: {T[0]}")
# nch0 = nchannels - 3
# # print(f"nchannels: {nchannels}")
# T[nchannels - 2] = 0
# # print(f"T[nchannels - 2]: {T[nchannels - 2]}")
# T[nchannels - 1] = 0
# # print(f"T[nchannels - 1]: {T[nchannels - 1]}")
#
# sn = 0
# # ii = 0
# for i in range(lvy):
#     sn = sn + vc[i]
#     # print(f"sn: {sn}")
#     # i = i + 1
#
# sm = 0
# # ii = 0
# for i in range(nchannels - 1):
#     # print(f"nchannels: {nchannels}")
#     # print(f"sm: {sm}")
#     # print(f"T[i]: {T[i]}")
#     sm = sm + T[i]
#     # print(f"sm*: {sm}")
#     # i = i + 1
#
# TV = [0] * nch0
# rTV = [0] * (nch0)
#
# # kk = 1
# for k in range(nch0 + 1):
#     if sm > 0:
#         TV[k - 1] = (T[k] / sm) * sn
#         # print(f"TV[k-1]: {TV[k-1]}")
#         if out_more:
#             # removal effects
#             rTV[k - 1] = T[k] / nconv
#             # print(f"rTV[k-1]: {rTV[k-1]}")
#     # kk = kk + 1
#
# VV = [0] * nch0
# rVV = [0] * nch0
#
# if flg_var_value:
#     V[0] = 0
#     V[nchannels - 2] = 0
#     V[nchannels - 1] = 0
#
#     sn = 0
#     # ii = 0
#     for i in range(lvy):
#         sn = sn + vv[i]
#         # i = i + 1
#
#     sm = 0
#     # ii = 0
#     for i in range(nchannels - 1):
#         sm = sm + V[i]
#         # i = i + 1
#
#     # kk = 1
#     for i in range(nch0 + 1):
#         if sm > 0:
#             VV[k - 1] = (V[k] / sm) * sn
#             if out_more:
#                 # removal effects
#                 rVV[k - 1] = V[k] / ssval
#         # kk = kk + 1
#
# vchannels0 = list(range(nch0))
# # kk = 1
# for k in range(nch0 + 1):
#     vchannels0[k - 1] = vchannels[k]
#     # kk = kk + 1
#
#     if flg_var_value:
#         if not out_more:
#             df = pd.DataFrame(
#                 {
#                     "channel_name": vchannels0,
#                     "total_conversion": TV,
#                     "total_conversion_value": VV
#                 }
#             )
#         else:
#             df = pd.DataFrame({
#                 "channel_name": vchannels0,
#                 "total_conversion": TV,
#                 "total_conversion_value": VV
#             })
#
#             re_df = pd.DataFrame({
#                 "channel_name": vchannels0,
#                 "removal_effects_conversion": rTV,
#                 "removal_effects_conversion_value": rVV
#             })
#
#             tmat = trans_mat.copy()
#     else:
#         if not out_more:
#             df = pd.DataFrame({
#                 "channel_name": vchannels0,
#                 "total_conversion": TV
#             })
#         else:
#             df = pd.DataFrame({
#                 "channel_name": vchannels0,
#                 "total_conversions": TV
#             })
#
#             re_df = pd.DataFrame({
#                 "channel_name": vchannels0,
#                 "removal_effects": rTV
#             })
#
#             tmat = trans_mat.copy()















































# # def markov_model(df, path_f, conv_f, rev_f, cost_f, null_f, order,
# #                  nsim, max_step, out_more, sep):
#
#
#
#
#
# r = markov_model(df, "path", "conversions", )
#




# def _get_transition_matrix(transitions, unique_channels):
#     """
#     Creates the transition matrix from the supplied transitions
#     and set of unique channels.
#
#     Adapted from: https://gist.github.com/tg12/d7efa579ceee4afbeaec97eb442a6b72
#     """
#     # n x n matrix
#     n = len(unique_channels)
#
#     M = [[0] * n for _ in range(n)]
#
#     for transition in transitions:
#         for (i,j) in zip(transition, transition[1:]):
#             M[i][j] += 1
#
#     for row in M:
#         s = sum(row)
#         if s > 0:
#             row[:] = [f / s for f in row]
#
#     return np.asarray(M)
#
#
# def _get_markov_components(df, path_f):
#     """Calculate the transition probability matrix for the given
#     paths."""
#     # get the paths
#     paths = df.loc[:, path_f].values
#
#     # container for the channels
#     channels = []
#
#     # iterate through the paths and append the channels
#     for path in paths:
#         for channel in path:
#             channels.append(channel)
#
#     # get a list of unique channels
#     unique_channels = np.unique(channels)
#
#     # map channel -> int for calculating the transition matrix
#     channel_mapper = {channel: i for i, channel in enumerate(
#         unique_channels)}
#
#     # unmap int -> channel
#     channel_unmapper = {v: k for k, v in channel_mapper.items()}
#
#     # container for the mapped paths
#     mapped_paths = []
#
#     # iterate through the paths and map them to ints
#     for i, path in enumerate(paths):
#         mapped_channels = []
#         for channel in path:
#             mapped_channels.append(channel_mapper[channel])
#         mapped_paths.append(mapped_channels)
#
#     # calculate the transition matrix
#     trans_mat = _get_transition_matrix(mapped_paths, unique_channels)
#
#     return trans_mat, channel_mapper, channel_unmapper
#
#
# def markov_memory(iterable, k_order):
#     """
#     Returns the ordered k_order tuples and number of occurrences of each
#     for the specified path.
#
#     Adapted from an itertools recipe.
#     """
#     a, b = itertools.tee(iterable)
#     ordered_pairs = list(zip(a, itertools.islice(b, 1, None)))
#     # d = dict(collections.Counter(ordered_pairs))
#     # e = collections.defaultdict(dict)
#     #
#     # for (c1, c2) in ordered_pairs:
#     #     e[c1] = collections.defaultdict(int)
#     #     e[c1][c2] += d[(c1, c2)]
#
#     # return d
#     return ordered_pairs
#
#
# def fit_markov(df, paths, conversions, sep, revenues=None, costs=None):
#     """Markov attribution model."""
#     trans_mat, channel_mapper, channel_unmapper = \
#         _get_markov_components(df, paths)
#
#     return trans_mat, channel_mapper, channel_unmapper
#

# print(df)
# print(re_df)
# print(tmat)

