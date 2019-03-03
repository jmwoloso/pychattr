"""
mixins.py: Mixin classes containing common functionality for the
various model specifications.
"""


class ChannelAttributionMixin(object):
    """
    Base class for the channel attribution models.
    """
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 separator=">>>"):
        self.paths = path_feature
        self.conversions = conversion_feature
        self.revenues = revenue_feature
        self.costs = cost_feature
        self.sep = separator

    def _derive_attributes(self, df):
        """Derives attributes used to identify which
        features are available to the Channel Attribution models."""
        self._paths = df.loc[:, self.paths].values
        self._conversions = df.loc[:, self.conversions].values
        self._revenues_ = df.loc[:, self.revenues].values if \
            self.revenues else None
        self._costs = df.loc[:, self.costs].values if self.costs else \
            None
