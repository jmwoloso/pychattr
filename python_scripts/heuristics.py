import pandas as pd

# def heuristic_models(df=None, first_touch=True, last_touch=True,
#                      linear_touch=True, path_feature=None,
#                      conversion_feature=None,
#                      conversion_value_feature=None,
#                      null_path_feature=None, separator=">",
#                      return_transition_probs=True,
#                      return_plot_data=True):

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


df = pd.read_csv("dev/data/example_data.csv",header=0)

df_ = heuristic_models(df=df,
                       path_feature="path",
                       conversion_feature="conversions",
                       separator=">")

df_.to_csv("dev/data/heuristic.csv",header=True,index=False)