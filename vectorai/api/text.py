import io
import base64
import requests
from typing import Dict, List
from .utils import retry

class ViTextClient:
    """
    Search and Encoding of Texts
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

    @retry()
    def search_text(
        self,
        collection_name: str,
        text,
        fields: List,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False
    ):
        """
Search a text field with text using Vector Search with text directly.

For example: "product_description" represents the description of a product::

    "AirPods deliver effortless, all-day audio on the go. And AirPods Pro bring Active Noise Cancellation to an in-ear headphone â€” with a customisable fit"

    -> <Encode the text to vector> ->

    i.e. text vector, "product_description_vector_": [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}

Args:
	text:
		Text to encode into vector and vector search with
	collection_name:
		Name of Collection
	search_fields:
		Vector fields to search through
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	page_size:
		Size of each page of results
	page:
		Page of the results
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	hundred_scale:
		Whether to scale up the metric by 100
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        return requests.post(
            url="{}/collection/search_with_text".format(self.url),
            json={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "text": text,
                "search_fields": fields,
                "metric": metric,
                "page": page,
                "page_size": page_size,
                "include_vector": include_vector,
                "include_count": include_count,
                "asc": asc
            },
        ).json()

    @retry()
    def encode_text(self, collection_name: str, text):
        """
Encode text into a vector

For example: a text field "product_description" represents the description of a product::

    "AirPods deliver effortless, all-day audio on the go. And AirPods Pro bring Active Noise Cancellation to an in-ear headphone â€” with a customisable fit"

    -> <Encode the text to vector> ->

    text vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

Args:
	text:
		Text to encode into vector
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/encode_text".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "text": text,
            },
        ).json()

    @retry()
    def encode_text_job(
        self, collection_name: str, text_field: str, refresh: bool = False
    ):
        """
Encode all texts in a field into vectors

Within a collection encode the specified text field in every document into vectors.

For example, a text field "product_description" represents the description of a product::

    document 1 text field: {"product_description" : "AirPods deliver effortless, all-day audio on the go. And AirPods Pro bring Active Noise Cancellation to an in-ear headphone â€” with a customisable fit."

    document 2 text field: {"product_description" : "MacBook Pro elevates the notebook to a whole new level of performance and portability. Wherever your ideas take you, youâ€™ll get there faster than ever with highâ€‘performance processors and memory, advanced graphics, blazingâ€‘fast storage and more â€” all in a compact package."

    -> <Encode the texts to vectors> ->

    document 1 text vector: {"product_description_vector_": [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]}

    document 2 text vector: {"product_description_vector_": [0.8364648222923279, 0.6280597448348999, 0.8112713694572449, 0.36105549335479736, 0.005313870031386614 ...]}

Args:
	text_field:
		The text field to encode into vectors
	refresh:
		Whether to refresh the whole collection and re-encode all to vectors
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/jobs/encode_text_field".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "text_field": text_field,
                "refresh": refresh,
            },
        ).json()
