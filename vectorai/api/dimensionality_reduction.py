import requests
from typing import List
from .utils import retry

class ViDimensionalityReductionClient:
    """
    Dimensionality Reduction
    """
    def __init__(self, username: str, api_key: str, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

    @retry()
    def dimensionality_reduce(
        self,
        collection_name: str,
        vectors: List[List[float]],
        vector_field: str,
        n_components: int,
        alias: str = "default",
    ):
        """
Trains a Dimensionality Reduction model on the collection

Dimensionality reduction allows your vectors to be reduced down to any dimensions greater than 0 using unsupervised machine learning. This is useful for even faster search and visualising the vectors.
        
Args:
	vector_field:
		Vector field to perform dimensionality reduction on
	alias:
		Alias is used to name the dimensionality reduced vectors
	n_components:
		The size/length to reduce the vector down to. If 0 is set then highest possible is of components is set, when this is done you can get reduction on demand of any length.
	refresh:
		Whether to refresh the whole collection and retrain the dimensionality reduction model
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/dimensionality_reduce".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vectors": vectors,
                "vector_field": vector_field,
                "alias": alias,
                "n_components": n_components,
            },
        ).json()

    @retry()
    def dimensionality_reduction_job(
        self,
        collection_name: str,
        vector_field: str,
        n_components: int = 0,
        alias: str = "default",
        refresh: bool = True,
    ):
        """
Trains a Dimensionality Reduction model on the collection

Dimensionality reduction allows your vectors to be reduced down to any dimensions greater than 0 using unsupervised machine learning. This is useful for even faster search and visualising the vectors.
        
Args:
	vector_field:
		Vector field to perform dimensionality reduction on
	alias:
		Alias is used to name the dimensionality reduced vectors
	n_components:
		The size/length to reduce the vector down to. If 0 is set then highest possible is of components is set, when this is done you can get reduction on demand of any length.
	refresh:
		Whether to refresh the whole collection and retrain the dimensionality reduction model
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/jobs/dimensionality_reduction".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "alias": alias,
                "n_components": n_components,
                "refresh": refresh,
            },
        ).json()
