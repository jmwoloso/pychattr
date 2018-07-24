import pandas as pd

from pychattr.channel_attribution import PyChAttr
from rpy2.robjects.packages import importr

import matplotlib.pyplot as plt
import seaborn as sns
# set the plot background
sns.set_style("darkgrid")

Rbase = importr("base")
RChannelAttribution = importr("ChannelAttribution")

df = pd.read_csv("demo_data.csv",
                 header=0)


pychattr_model = PyChAttr(df=df,
                          markov_model=True,
                          heuristic_model=True,
                          first_touch=True,
                          last_touch=True,
                          linear_touch=True,
                          path_feature="path",
                          conversion_feature="total_conversions",
                          conversion_value_feature="total_conversion_value",
                          null_path_feature="total_null",
                          separator=">",
                          order=1,
                          n_simulations=None,
                          max_step=None,
                          return_transition_probs=True,
                          random_state=26,
                          return_plot_data=True)

pychattr_model.fit()

# many of the attributes are just dataframes with the model results
model = pychattr_model.model_
transition_matrix = pychattr_model.transition_matrix_
removal_effects = pychattr_model.removal_effects_

markov = pychattr_model.markov_
heuristic = pychattr_model.heuristic_

conversion_features = pychattr_model.conversion_features_
conversion_value_features = pychattr_model.conversion_value_features_
conv_df = pychattr_model.melted_data_[0]
conv_val_df = pychattr_model.melted_data_[1]

plt.figure(figsize=(20, 10))

# plot the bars
sns.barplot(x="channel name",
            y="total conversions",
            hue="model heuristic",
            data=conv_df)
plt.xlabel("Channel Name",
           size=20,
           weight="bold")
plt.ylabel("Conversions",
           size=20,
           weight="bold")
plt.title("Total Conversions",
          size=30,
          weight="bold")
plt.show()

plt.figure(figsize=(20, 10))
# plot the bars
sns.barplot(x="channel name",
            y="total conversion value",
            hue="model heuristic",
            data=conv_val_df)
plt.xlabel("Channel Name",
           size=20,
           weight="bold")
plt.ylabel("Conversion Value",
           size=20,
           weight="bold")
plt.title("Total Conversion Value",
          size=30,
          weight="bold")
plt.show()





