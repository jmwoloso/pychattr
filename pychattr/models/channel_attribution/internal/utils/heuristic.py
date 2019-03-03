"""
heuristic.py: Various utility functions used during construction of
the heuristic models.
"""
from ..logic.heuristic import first_touch_model, last_touch_model, \
    linear_touch_model, time_decay_model, u_shaped_model, \
    w_shaped_model, z_shaped_model, ensemble_model


def fit_heuristic_models(heuristics):
    """
    Fits the specified heuristic models.
    """
    for heuristic in heuristics:
        results = {}
        if heuristic == "linear_touch":
            model = first_touch_model()
        if heuristic == "last_touch":
            model = last_touch_model()
        if heuristic == "linear_touch":
            model = linear_touch_model()
        if heuristic == "time_decay":
            model = time_decay_model()
        if heuristic == "u_shaped":
            model = u_shaped_model()
        if heuristic == "w_shaped":
            model = w_shaped_model()
        if heuristic == "z_shaped":
            model = z_shaped_model()

        # the results of the current model to the results dict
        results[heuristic] = model

        # fit the ensemble model if specified
        if heuristic == "ensemble_model":
            pass



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





def _validate_heuristic_inputs():
    """Validates the inputs"""
    pass

