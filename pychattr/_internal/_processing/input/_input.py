"""
_input.py: Processing routines for dataframe inputs
"""


def _convert_to_required_dtypes(df, paths, conversions,
                                revenues=None, costs=None):
    """Utility function that takes values and checks whether they can
    have the specified type applied, if so it applies them."""
    try:
        values = values.astype(type)
        return values
    except ValueError as e:
        raise ValueError("`{}` must be type `{}` or convertible to "
                         "that type".format(name, type))


def _aggregate_paths(df, path_feature, conversion_feature,
                     revenue_feature=None, cost_feature=None):
    """Group by path and aggregate the other features."""
    # if we have revenues and costs
    if revenue_feature and cost_feature:
        # attempt dtype conversion
        df = _convert_to_required_dtypes(df, path_feature,
                                         conversion_feature,
                                         revenues=None,
                                         costs=None)

        gb = df.groupby([path_feature], as_index=False).agg(
            {
                conversion_feature: "sum",
                revenue_feature: "sum",
                cost_feature: "sum"
            }
        )
    # if we only have revenues
    elif revenue_feature:
        gb = df.groupby([path_feature], as_index=False).agg(
            {
                conversion_feature: "sum",
                revenue_feature: "sum"
            }
        )
    # if we only have costs
    elif cost_feature:
        gb = df.groupby([path_feature], as_index=False).agg(
            {
                conversion_feature: "sum",
                cost_feature: "sum"
            }
        )
    # if we have neither revenues nor costs
    else:
        gb = df.groupby([path_feature], as_index=False).agg(
            {
                conversion_feature: "sum"
            }
        )

    return gb
