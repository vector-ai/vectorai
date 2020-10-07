"""Mixin class for analytics submodule containing vector analytics tools.
"""

from .dimensionality_reduction import *
from .viz import *
from .tables import *

class ViAnalyticsMixin(VizMixin, TableMixin):
    """
    Vi Analytics Mixin.
    Currently includes visualisation mixin. 
    """

    pass
