import pytest
import pandas as pd

from .._input import _aggregate_paths


def make_dataframe(with_revenues=False, with_costs=False):
    """Test fixtures for use by the tests."""
    data = {
        "paths": ["a", "a"],
        "conversions": ["1", "1"]
    }
    if with_revenues and with_costs:
        data["revenues"] = ["1", "1"]
        data["costs"] = ["1", "1"]
    elif with_revenues:
        data["revenues"] = ["1", "1"]
    elif with_costs:
        data["costs"] = ["1", "1"]
    else:
        pass

    return pd.DataFrame(data)


dataframes = (make_dataframe(with_revenues=True, with_costs=True),
              make_dataframe(with_revenues=True),
              make_dataframe(with_costs=True),
              make_dataframe())


@pytest.mark.input
class TestAggregatePaths():
    """Tests the path aggregation utility function in a variety of
    settings.."""
    def test_revenues_and_costs(self):
        """Tests the scenario when revenues and costs are present."""
        df = dataframes[0]
        gb = _aggregate_paths(df, "paths", "conversions",
                              revenue_feature="revenues",
                              cost_feature="costs")
        conversions = gb.loc[:, "conversions"].values[0]
        revenues = gb.loc[:, "revenues"].values[0]
        costs = gb.loc[:, "costs"].values[0]

        assert revenues == 2 and costs == 2 and conversions == 2

    def test_revenues_only(self):
        """Tests the scenario when only revenues are present."""
        df = dataframes[0]
        gb = _aggregate_paths(df, "paths", "conversions",
                              revenue_feature="revenues")
        conversions = gb.loc[:, "conversions"].values[0]
        revenues = gb.loc[:, "revenues"].values[0]

        assert revenues == 2 and conversions == 2

    def test_costs_only(self):
        """Tests the scenario when only costs are present."""
        df = dataframes[0]
        gb = _aggregate_paths(df, "paths", "conversions",
                              cost_feature="costs")
        conversions = gb.loc[:, "conversions"].values[0]
        costs = gb.loc[:, "costs"].values[0]

        assert costs == 2 and conversions == 2

    def test_no_revenues_no_costs(self):
        """Tests the scenario when revenues and costs are not
        present."""
        df = dataframes[0]
        gb = _aggregate_paths(df, "paths", "conversions")
        conversions = gb.loc[:, "conversions"].values[0]

        assert conversions == 2

    def test_missing_positional_args(self):
        """Tests that a TypeError is thrown when positional arguments
        are not specified as required."""
        with pytest.raises(TypeError):
            _aggregate_paths()
