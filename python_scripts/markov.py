



# class PyChAttr(object):
#     def __init__(self, df=None, markov_model=True, heuristic_model=True,
#                  first_touch=True, last_touch=True,
#                  linear_touch=True, path_feature=None,
#                  conversion_feature=None, conversion_value_feature=None,
#                  null_path_feature=None, separator=">", order=1,
#                  n_simulations=None, max_step=None,
#                  return_transition_probs=True, random_state=None,
#                  return_plot_data=True):



def markov_model(df=None, path_feature=None, conversion_feature=None,
                 revenue_feature=None, cost_feature=None,
                 null_path_feature=None, separator=">", order=1,
                 n_simulations=1000, max_step=None,
                 return_transition_probs=True,
                 return_plot_data=False, random_state=None):
    """Hidden Markov Model for Attribution."""
    has_revenue = True if revenue_feature else False
    has_cost = True if cost_feature else False
    has_nulls = True if null_path_feature else False
    path_values = df.loc[:, path_feature].values
    conversion_values = df.loc[:, conversion_feature].values
    revenue_values = df.loc[:, revenue_feature].values if has_revenue \
        else None
    cost_values = df.loc[:, cost_feature].values if has_cost else None


    touch_point_dict = {}



