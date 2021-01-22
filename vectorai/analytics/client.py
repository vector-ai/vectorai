from .comparator import ComparatorClient

class ViAnalyticsClient(ComparatorClient):
    def __init__(self, username: str=None, api_key: str=None, url="https://vector-analytics.vctr.ai"):
        self.url = url
        self.username = username
        self.api_key = api_key
