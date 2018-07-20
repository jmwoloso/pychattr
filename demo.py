import pandas as pd

from pychattr.channel_attribution import PyChAttr

df = pd.read_csv("demo_data.csv",
                 header=0)


pychattr_model = PyChAttr(df=df,
                          model_type="both",
                          model_paradigm="all",
                          path_feature="path",
                          conversion_feature="total_conversions",
                          conversion_value_feature="total_conversion_value",
                          null_path_feature="total_null",
                          separator=">",
                          order=1,
                          n_simulations=None,
                          max_step=None,
                          return_transition_probs=True,
                          random_state=26)

pychattr_model.fit()

# many of the attributes are just dataframes with the model results
model = pychattr_model.model_
transition_matrix = pychattr_model.transition_matrix_
removal_effects = pychattr_model.removal_effects_

