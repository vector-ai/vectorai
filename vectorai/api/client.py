from .api import _ViAPIClient
from .cluster import *
from .text import *
from .audio import *
from .image import *
from .dimensionality_reduction import *

class ViAPIClient(_ViAPIClient, ViDimensionalityReductionClient, ViTextClient, ViAudioClient, ViImageClient, ViClusterClient):
    def __init__(self, username, api_key, url="https://api.vctr.ai"):
        self.username = username
        self.api_key = api_key
        self.url = url
