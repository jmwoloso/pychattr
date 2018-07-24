# R Library Requirements

In addition to having base R installed, the following additional libraries are required to make use of this package:

```
ChannelAttribution
```


# Python Requirements

The following python package versions were installed when I created this library, so your mileage may vary when attempting to use differing versions.

```
Cython>=0.28.2

pandas>=0.23.3

matplotlib>=2.2.2

rpy>=2.9.4
```

# Additional Items of Note

With this version of rpy2, you might see warnings about using a deprecated method within pandas. This stems from the following code within `/site-packages/rpy2/robjects/pandas2ri.py` of your python installation:


```
@ri2py.register(DataFrame)
def ri2py_dataframe(obj):
    items = tuple((k, ri2py(v)) for k, v in obj.items())
    res = PandasDataFrame.from_items(items)
    return res
```


If the warning annoys you, just replace the relevant section of code (starting at line 188) with the following to correct the warning:

```
@ri2py.register(DataFrame)
def ri2py_dataframe(obj):
    items = tuple((k, ri2py(v)) for k, v in obj.items())
    # res = PandasDataFrame.from_items(items)
    res = PandasDataFrame.from_dict(OrderedDict(items))
    return res
```
