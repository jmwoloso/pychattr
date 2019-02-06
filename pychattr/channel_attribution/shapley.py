from itertools import chain, combinations, permutations
import pandas as pd

# from pychattr.utils import OrderedSet

#TODO: remove and use utils.classes implementation
import collections


class OrderedSet(collections.MutableSet):
    """Based on the recipe for an OrderedSet found at:
    https://code.activestate.com/recipes/576694/"""

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


def create_combinations():
    pass


def powerset_generator(coalition=None, separator=" > ",
                       order_matters=False):
    touchpoints = coalition.split(separator)
    if order_matters is False:
        subsets = chain.from_iterable(
            combinations(
                touchpoints,
                n
            ) for n in range(
                len(touchpoints) + 1
            )
        )
    elif order_matters is True:
        subsets = chain.from_iterable(
            permutations(
                touchpoints,
                n
            ) for n in range(
                len(touchpoints) + 1
            )
        )
    # do we need to throw off the empty set?
    next(subsets)
    return subsets


def create_coalitions(path=None, separator=None, order_matters=False):
    """Function to take a path and return a corresponding coalition"""
    # separate the paths into the touchpoints
    # TODO: implement flavor where ordering is important
    if order_matters is True:
        # raise NotImplementedError("`order_invariant=False` is not "
        #                           "currently implemented")
        # create each coalition using ordered sets
        # list of the touchpoints for a given path
        touchpoints = path.split(separator)
        if len(touchpoints) == 0:
            return
        elif len(touchpoints) == 1:
            return touchpoints[0]
        else:
            # ordered set
            coalition = list(OrderedSet(touchpoints))
            return "{}".format(separator).join(coalition)
    elif order_matters is False:
        touchpoints = path.split(separator)
        # sort to ensure sets match
        touchpoints.sort()
        # if there is nothing in the path we return nothing
        if len(touchpoints) == 0:
            return
        # if the path contains a single touchpoint, we're done
        elif len(touchpoints) == 1:
            return touchpoints[0]
        else:
            # remove redundant touchpoints to create the coalition
            coalition = list(set(touchpoints))
            # sort the coalition and return it
            coalition.sort()
            return "{}".format(separator).join(coalition)

def calculate_coalition_values(coalitions=None, order_matters=False):
    pass











def shapley_model(df=None, path_feature=None,
                  conversion_feature=None,
                  conversion_value_feature=None,
                  null_path_feature=None,
                  order_matters=False, separator=None,
                  return_plot_data=True):
    """Function to create the specified flavor of Shapley model."""
    # create the coalitions from the paths in the dataframe
    df_ = df.copy()
    df_.loc[:, "coalition"] = df_.loc[:, path_feature].map(
        lambda path: create_coalitions(path=path,
                                       separator=separator,
                                       order_matters=order_matters)
    )

    # condense the coalition values
    gb_features = [
        conversion_feature,
    ]

    # add the value feature
    if conversion_value_feature is not None:
        gb_features.append(conversion_value_feature)

    # add the null feature
    if null_path_feature is not None:
        gb_features.append(null_path_feature)

    # sum the rows when combining
    gb_aggregates = {feature: "sum" for feature in gb_features}

    # groupby coalition and aggregate values
    gb = df_.groupby("coalition", as_index=False).agg(
        gb_aggregates
    )

    # create a dict to hold the inputs to the shapley values
    shapley_inputs_dict = {coalition: list()
                           for coalition
                           in gb.loc[:, "coalition"].tolist()}

    # create a dict to hold the shapley values
    shapley_values_dict = dict()

    # work through each touchpoint; the summands for the shapley value
    # start with all the coalitions that the touchpoint is not a part of


#TODO: remove
df = pd.read_csv("dev/data/free_trial_and_demo_path_data_final.csv.gz",
                 header=0,
                 compression="gzip")

df.loc[:, "coalition"] = df.loc[:, "path"].map(
    lambda path: create_coalitions(path=path,
                                   separator=" > ",
                                   order_matters=False)
)

aggs = {"total_conversions": "sum"}

# group by coalition now
gb = df.groupby("coalition", as_index=False).agg(aggs)

gb.loc[:, "coalition"]


