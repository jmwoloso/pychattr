

from .mixins import ChannelAttributionMixin

class MarkovModel(ChannelAttributionMixin):
    def __init__(self, path_feature, conversion_feature,
                 revenue_feature=None, cost_feature=None,
                 separator=">>>"):
        """
        Class for Markov channel attribution model.
        """
        super().__init__(path_feature, conversion_feature,
                         revenue_feature=revenue_feature,
                         cost_feature=cost_feature, separator=separator)

    def fit(self, df):
        """

        Parameters
        ----------
        dataframe: pandas.DataFrame; required.
            The dataframe containing the path data to be modeled.

        Returns
        -------
        self: returns an instance of self.
        """
        # derive the feature attributes
        self._derive_attributes(df)
