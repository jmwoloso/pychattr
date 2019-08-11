# README

This is a Python implementation based on the ChannelAttribution package in R developed by Davide Altomare and David Loris.

https://cran.r-project.org/web/packages/ChannelAttribution/ChannelAttribution.pdf



# Installation
```pip install pychattr```


# Markov Model
```
import pandas as pd
from pychattr.channel_attribution import MarkovModel

data = {
    "path": [
        "A >>> B >>> A >>> B >>> B >>> A",
        "A >>> B >>> B >>> A >>> A",
        "A >>> A"
    ],
    "conversions": [1, 1, 1],
    "revenue": [1, 1, 1],
    "cost": [1, 1, 1]
}

df = pd.DataFrame(data)

path_feature="path"
conversion_feature="conversions"
null_feature=None
revenue_feature="revenue"
cost_feature="cost"
separator=">>>"
k_order=1
n_simulations=10000
max_steps=None
return_transition_probs=True
random_state=26

# instantiate the model
mm = MarkovModel(path_feature=path_feature,
                 conversion_feature=conversion_feature,
                 null_feature=null_feature,
                 revenue_feature=revenue_feature,
                 cost_feature=cost_feature,
                 separator=separator,
                 k_order=k_order,
                 n_simulations=n_simulations,
                 max_steps=max_steps,
                 return_transition_probs=return_transition_probs,
                 random_state=random_state)

# fit the model
mm.fit(df)
```

```
# view the simulation results
print(mm.attribution_model_)
```
```
  channel_name  total_conversions
0            A           1.991106
1            B           1.008894
```

```
# view the transition matrix
print(mm.transition_matrix_)
```
```
  channel_from    channel_to  transition_probability
0      (start)             A                     1.0
1            A             B                     0.5
2            A  (conversion)                     0.5
3            B             A                     1.0
```

```
# view the removal effects
print(mm.removal_effects_)
```

```
  channel_name  removal_effect
0            A          1.0000
1            B          0.5067
```



# Heuristic Model
```
import pandas as pd
from pychattr.channel_attribution import HeuristicModel

data = {
    "path": [
        "A >>> B >>> A >>> B >>> B >>> A",
        "A >>> B >>> B >>> A >>> A",
        "A >>> A"
    ],
    "conversions": [1, 1, 1],
    "revenue": [1, 1, 1],
    "cost": [1, 1, 1]
}

df = pd.DataFrame(data)

path_feature="path"
conversion_feature="conversions"
null_feature=None
revenue_feature="revenue"
cost_feature="cost"
separator=">>>"
first_touch=True
last_touch=True
linear_touch=True
ensemble_results=True

# instantiate the model
hm = HeuristicModel(path_feature=path_feature,
                    conversion_feature=conversion_feature,
                    null_feature=null_feature,
                    revenue_feature=revenue_feature,
                    cost_feature=cost_feature,
                    separator=separator,
                    first_touch=first_touch,
                    last_touch=last_touch,
                    linear_touch=linear_touch,
                    ensemble_results=ensemble_results)

# fit the model
hm.fit(df)
```

```
# view the heuristic results
print(hm.attribution_model_)
```
```
  channel  first_touch_conversions  ...  ensemble_revenue  ensemble_cost
0       A                      3.0  ...               8.1            5.1
1       B                      0.0  ...               0.9            0.9
[2 rows x 13 columns]
```