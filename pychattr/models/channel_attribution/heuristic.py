"""
heuristic.py: contains the class wrapper for the heuristic models 
used in channel attribution.

see: https://www.bizible.com/blog/multi-touch-attribution-full-debrief
"""
from pychattr._internal._utils import ChannelAttributionMixin


def _first_touch():
    """First-touch attribution model."""
    pass

def _last_touch():
    """Last-touch attribution model."""
    pass

def _linear_touch():
    """Linear touch attribution model."""
    pass

def _time_decay():
    """Time decay attribution model."""
    pass

def _u_shaped():
    """U-shaped attribution model."""
    pass

def _w_shaped():
    """W-shaped attribution model."""
    pass

def _z_shaped():
    """Z-shaped (full path) attribution model."""
    pass

def _ensemble():
    """Blended version of all the selected heuristic models."""
    pass


class HeurisiticModel(ChannelAttributionMixin):
    """
    Class wrapper for the heuristic channel attribution models.

    Parameters
    ----------
        path_feature: string; required.
        The name of the feature containing the paths.

    conversion_feature: string; required.
        The name of the feature containing the number of
        conversions for each path.

    revenue_feature: string; optional.
        The name of the feature containing the revenue generated
        for each path.

    cost_feature: string; optional.
        The name of the feature containing the cost incurred for
        each path.

    separator: string; required.
        The symbol used to separate the touch points in each path.

    first_touch: boolean; required.
        Whether to calculate the first-touch heuristic model.

    last_touch: boolean; required.
        Whether to calculate the last-touch heuristic model.

    linear_touch: boolean; required.
        Whether to calculate the linear-touch heuristic model.

    time_decay: boolean; required.
        Whether to calculate the time-decay heuristic model.

    u_shaped: boolean; required.
        Whether to calculate the u-shaped heuristic model.

    w_shaped: boolean; required.
        Whether to calculate the w-shaped heuristic model.

    z_shaped: boolean; required.
        Whether to calculate the z-shaped heuristic model.

    ensemble_results: boolean; required.
        Whether to create an ensemble of the resulting models.

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
                 separator=">>>", first_touch=True,
                 last_touch=True, linear_touch=True, time_decay=True,
                 u_shaped=True, w_shaped=True, z_shaped=True,
                 ensemble_results=True):
        super().__init__(path_feature, conversion_feature,
                         revenue_feature, cost_feature, separator)

        self.first = first_touch
        self.last = last_touch
        self.linear = linear_touch
        self.time = time_decay
        self.u = u_shaped
        self.w = w_shaped
        self.z = z_shaped
        self.ensemble = ensemble_results

    def fit(self, dataframe=None):
        """Fit the specified heuristic models."""
        # self._
        # derive attributes that will be used during model construction
        self._derive_attributes(dataframe)

        # attempt to convert the values to the types required for
        # modeling

        # container to hold the resulting models
        self.results_ = None


    def _derive_attributes(self, df):
        """Derives attributes used to identify which components to
        include in the heuristic model."""
        self._paths = df.loc[:, self.paths].values
        self._conversions = df.loc[:, self.conversions].values
        self._revenues_ = df.loc[:, self.revenues].values if \
            self.revenues else None
        self._costs = df.loc[:, self.costs].values if self.costs else\
            None




def heuristic_models(df=None, path_feature=None,
                     conversion_feature=None, revenue_feature=None,
                     cost_feature=None, separator=">"):
    """Traditional heuristic models (first-touch, last-touch,
    linear-touch)."""

    def make_touch_point_dict(touch_point):
        """Returns the template for accumulating touch_point values."""
        return {
            "channel_name": touch_point,
            "first_touch_conversions": 0,
            "first_touch_revenue": 0,
            "first_touch_cost": 0,
            "last_touch_conversions": 0,
            "last_touch_revenue": 0,
            "last_touch_cost": 0,
            "linear_touch_conversions": 0,
            "linear_touch_revenue": 0,
            "linear_touch_cost": 0
        }

    def get_touch_point_values(touch_point_dict, touch_point,
                               conversion_value, revenue_value,
                               cost_value, heuristic):
        """Returns the values for each of the attribution heuristics."""
        # first-touch
        conversion_key = "{}_touch_conversions".format(heuristic)

        if revenue_value:
            revenue_key = "{}_touch_revenue".format(heuristic)

        if cost_value:
            cost_key = "{}_touch_cost".format(heuristic)

        if heuristic in ["first", "last"]:
            touch_point_dict[touch_point][conversion_key] += \
                conversion_value

            if revenue_value:
                touch_point_dict[touch_point][revenue_key] += \
                    revenue_value

            if cost_value:
                touch_point_dict[touch_point][cost_key] += \
                    cost_value

        elif heuristic == "linear":
            conversion_value = conversion_value / len(touch_point)

            for tp in touch_point:
                touch_point_dict[tp][conversion_key] += \
                    conversion_value

                if revenue_value:
                    revenue_value = revenue_value / len(touch_point)
                    touch_point_dict[tp][revenue_key] += revenue_value

                if cost_value:
                    cost_value = cost_value / len(touch_point)
                    touch_point_dict[tp][cost_key] += cost_value

        return touch_point_dict

    has_revenue = True if revenue_feature else False
    has_cost = True if cost_feature else False
    path_values = df.loc[:, path_feature].values
    conversion_values = df.loc[:, conversion_feature].values
    revenue_values = df.loc[:, revenue_feature].values if \
        has_revenue else None
    cost_values = df.loc[:, cost_feature].values if has_cost else None

    touch_point_dict = {}

    # iterate through the paths
    for i in range(len(path_values)):
        # split on the separator
        touch_points = path_values[i].split(separator)
        # iterate on the split touch_points
        for touch_point in touch_points:
            # if the touch_point isn't in the unique list, add it
            if touch_point not in touch_point_dict.keys():
                touch_point_dict[touch_point] = make_touch_point_dict(
                    touch_point)

        for touch_point, heuristic in zip([touch_points[0],
                                           touch_points[-1],
                                           touch_points],
                                          ["first", "last", "linear"]):
            if has_revenue and has_cost:
                touch_point_dicts = \
                    get_touch_point_values(touch_point_dict,
                                           touch_point,
                                           conversion_values[i],
                                           revenue_values[i],
                                           cost_values[i],
                                           heuristic)
            elif has_revenue and not has_cost:
                touch_point_dicts = \
                    get_touch_point_values(touch_point_dict,
                                           touch_point,
                                           conversion_values[i],
                                           revenue_values[i],
                                           cost_values,
                                           heuristic)
            elif has_cost and not has_revenue:
                touch_point_dicts = \
                    get_touch_point_values(touch_point_dict,
                                           touch_point,
                                           conversion_values[i],
                                           revenue_values,
                                           cost_values[i],
                                           heuristic)
            else:
                touch_point_dicts = \
                    get_touch_point_values(touch_point_dict,
                                           touch_point,
                                           conversion_values[i],
                                           revenue_values,
                                           cost_values,
                                           heuristic)

    return pd.DataFrame(list(touch_point_dicts.values()))


df = pd.read_csv("dev/data/example_data.csv", header=0)

df_ = heuristic_models(df=df,
                       path_feature="path",
                       conversion_feature="conversions",
                       separator=">")

df_.to_csv("dev/data/heuristic.csv", header=True, index=False)