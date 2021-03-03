from .api import *
from .cluster import *
from .text import *
from .audio import *
from .image import *
from .dimensionality_reduction import *

class ViAPIClient(_ViAPIClient, ViDimensionalityReductionClient, ViTextClient, ViAudioClient, ViImageClient, ViClusterClient):
    pass
