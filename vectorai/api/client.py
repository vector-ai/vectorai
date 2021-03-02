import json 
from .api import _ViAPIClient
from .cluster import ViClusterClient
from .dimensionality_reduction import ViDimensionalityReductionClient
from .image import ViImageClient
from .audio import ViAudioClient
from .tedt import ViTextClient

class ViAPIClient(_ViAPIClient, ViClusterClient, ViDimensionalityReductionClient, ViImageClient, ViAudioClient, ViTextClient):

    def __init__(self, username, api_key, url="https://api.vctr.ai"):
        self.username = username
        self.api_key = api_key
        self.url = url
