"""
heuristic.py: Various utility functions used during construction of
the heuristic models.
"""
from ..logic.heuristic import fit_model


def fit_heuristic_models(heuristics, paths, conversions,
                         revenues, costs, separator):
    """
    Fits the specified heuristic models.
    """
    for heuristic in heuristics:
        results = {}
        if heuristic == "ensemble_model":
            # TODO: might want to break this out of the partial
            #  application function (fit_model)
            model = fit_model(paths, conversions, revenues, costs,
                              separator, heuristic=heuristic)

        model = fit_model(paths, conversions, revenues, costs,
                          separator, heuristic=heuristic)

        # the results of the current model to the results dict
        results[heuristic] = model

        return results


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
