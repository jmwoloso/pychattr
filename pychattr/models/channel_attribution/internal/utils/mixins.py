"""
mixins.py: Mixin classes containing common functionality for the
various model specifications.
"""


class ChannelAttributionMixin(object):
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 separator=">>>"):
        self.paths = path_feature
        self.conversions = conversion_feature
        self.revenues = revenue_feature
        self.costs = cost_feature
        self.sep = separator

    def _get_internals(self, df):
        """Derives internal attributes used during model
        construction."""
        # aggregate the paths
        df_ = df.copy()
        aggregations = {
            self.conversions: "sum",
        }
        if self.revenues:
            aggregations[self.revenues] = "sum"
        if self.costs:
            aggregations[self.costs] = "sum"

        self.df_ = df_.groupby([self.paths], as_index=False).agg(
            aggregations)


class HeuristicModelMixin(ChannelAttributionMixin):
    def _get_internals(self, df):
        """Extends the inherited method for heuristic-specifc
        internals."""
        # call to parent method
        super()._get_internals(df)

        # extensions
        heuristics = []
        if self.first:
            heuristics.append("first_touch")
        if self.last:
            heuristics.append("last_touch")
        if self.linear:
            heuristics.append("linear_touch")
        if self.time:
            heuristics.append("time_decay")
        if self.u:
            heuristics.append("u_shaped")
        if self.w:
            heuristics.append("w_shaped")
        if self.z:
            heuristics.append("z_shaped")
        if self.ensemble:
            heuristics.append("ensemble_model")
        self._heuristics = heuristics

        return self


class MarkovModelMixin(ChannelAttributionMixin):
    def _get_internals(self, df):
        """Extends the inherited method for markov-specific
        internals."""
        pass
