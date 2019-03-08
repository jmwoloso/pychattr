"""
Wrapper class for the Shapley model.
"""
# Author: Abhi Sivasailam
# License: BSD 3-clause

from ._mixins import ShapleyMixin


class ShapleyModel(ShapleyMixin):
    def __init__(self):
        """
        Your elegant interface here :)
        """
        raise NotImplementedError("This class is currently under "
                                  "development and will be available "
                                  "with the next minor release.")
