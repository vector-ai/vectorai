import os
from .comparator import ComparatorClient

class ViAnalyticsClient(ComparatorClient):
    def __init__(self, username: str=None, api_key: str=None, 
    url: str = "https://api.vctr.ai", analytics_url="https://vector-analytics.vctr.ai"):
        self.username = username if username is not None else os.environ['VI_USERNAME']
        self.api_key = api_key if api_key is not None else os.environ['VI_API_KEY']
        self.url = url
        self.analytics_url = analytics_url
