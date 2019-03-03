"""
heuristic.py: Various utility functions used during construction of
the heuristic models.
"""


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








def _validate_heuristic_inputs():
    """Validates the inputs"""
    pass

