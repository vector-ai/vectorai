import io
import base64
import requests
from typing import Dict, List
from .utils import retry, return_curl_or_response

class ViArrayDictClient:
    """
    Search and Encoding for Array & Dictionary
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

    @retry()
    def encode_dictionary_field(self, collection_name: str, dictionary_fields: List, return_curl: bool=False, **kwargs):
        """
Encode all dictionaries in a field for collection into vectors

Within a collection encode the specified dictionary field in every document into vectors.

For example: a dictionary that represents a **person's characteristics visiting a store, field "person_characteristics"**::

    document 1 field: {"person_characteristics" : {"height":180, "age":40, "weight":70}}

    document 2 field: {"person_characteristics" : {"age":32, "purchases":10, "visits": 24}}

    -> <Encode the dictionaries to vectors> ->

    | height | age | weight | purchases | visits |
    |--------|-----|--------|-----------|--------|
    | 180    | 40  | 70     | 0         | 0      |
    | 0      | 32  | 0      | 10        | 24     |

    document 1 dictionary vector: {"person_characteristics_vector_": [180, 40, 70, 0, 0]}

    document 2 dictionary vector: {"person_characteristics_vector_": [0, 32, 0, 10, 24]}

Args:
    dictionary_fields:
        The dictionary field to train on to encode into vectors
    collection_name:
        Name of Collection
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "dictionary_fields": dictionary_fields,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/encode_dictionary_field".format(self.url),
            params=params,
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def encode_dictionary(self, collection_name: str, dictionary: Dict, dictionary_field: str, return_curl=False, **kwargs):
        """
Encode an dictionary into a vector

For example: a dictionary that represents a **person's characteristics visiting a store, field "person_characteristics"**::

    {"height":180, "age":40, "weight":70}

    -> <Encode the dictionary to vector> ->

    | height | age | weight | purchases | visits |
    |--------|-----|--------|-----------|--------|
    | 180    | 40  | 70     | 0         | 0      |

    dictionary vector: [180, 40, 70, 0, 0]

Args:
	collection_name:
		Name of Collection
	dictionary:
		A dictionary to encode into vectors
	dictionary_field:
		The dictionary field that encoding of the dictionary is trained on
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "dictionary": dictionary,
            "dictionary_field": dictionary_field,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/encode_dictionary".format(self.url),
            json=params,
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def search_with_dictionary(self, collection_name: str, dictionary: Dict, dictionary_field: str,
        fields: List,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False, **kwargs):
        """
Search a dictionary field with a dictionary using Vector Search with a dictionary directly.

For example: a dictionary that represents a **person's characteristics visiting a store, field "person_characteristics"**::

    {"height":180, "age":40, "weight":70}

    -> <Encode the dictionary to vector> ->

    | height | age | weight | purchases | visits |
    |--------|-----|--------|-----------|--------|
    | 180    | 40  | 70     | 0         | 0      |

    dictionary vector: [180, 40, 70, 0, 0]

    -> <Vector Search> ->

    Search Results: {...}

Args:
	collection_name:
		Name of Collection
	search_fields:
		Vector fields to search against
	page_size:
		Size of each page of results
	page:
		Page of the results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
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
	dictionary:
		A dictionary to encode into vectors
	dictionary_field:
		The dictionary field that encoding of the dictionary is trained on
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "dictionary": dictionary,
            "dictionary_field": dictionary_field,
            "sum_fields": sum_fields,
            "search_fields": fields,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "asc": asc,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/search_with_dictionary".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def encode_array_field(self, collection_name: str, array_fields: List, return_curl: bool=False, **kwargs):
        """
Encode all arrays in a field for a collection into vectors

Within a collection encode the specified array field in every document into vectors.

For example, array that represents a ****movie's categories, field "movie_categories"**::

    document 1 array field: {"category" : ["sci-fi", "thriller", "comedy"]}

    document 2 array field: {"category" : ["sci-fi", "romance", "drama"]}

    -> <Encode the arrays to vectors> ->

    | sci-fi | thriller | comedy | romance | drama |
    |--------|----------|--------|---------|-------|
    | 1      | 1        | 1      | 0       | 0     |
    | 1      | 0        | 0      | 1       | 1     |

    document 1 array vector: {"movie_categories_vector_": [1, 1, 1, 0, 0]}

    document 2 array vector: {"movie_categories_vector_": [1, 0, 0, 1, 1]}

Args:
	array_fields:
		The array field to train on to encode into vectors
	collection_name:
		Name of Collection
"""

        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "array_fields": array_fields
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/encode_array_field".format(self.url),
            params=params,
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def encode_array(self, collection_name: str, array: List, array_field: str, return_curl: bool=False, **kwargs):
        """
Encode an array into a vector

For example: an array that represents a **movie's categories, field "movie_categories"**::

    ["sci-fi", "thriller", "comedy"]

    -> <Encode the arrays to vectors> ->

    | sci-fi | thriller | comedy | romance | drama |
    |--------|----------|--------|---------|-------|
    | 1      | 1        | 1      | 0       | 0     |

    array vector: [1, 1, 1, 0, 0]

Args:
	array_field:
		The array field that encoding of the dictionary is trained on
	array:
		The array to encode into vectors
	collection_name:
		Name of Collection
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "array": array,
            "array_field": array_field,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/encode_array".format(self.url),
            params=params,
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_with_array(self, collection_name: str, array: List, array_field: str,
        fields: List,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False, 
        return_curl: bool=False, 
        **kwargs):
        """
Search an array field with an array using Vector Search with an array directly.

For example: an array that represents a **movie's categories, field "movie_categories"**::

    ["sci-fi", "thriller", "comedy"]

    -> <Encode the arrays to vectors> ->

    | sci-fi | thriller | comedy | romance | drama |
    |--------|----------|--------|---------|-------|
    | 1      | 1        | 1      | 0       | 0     |

    array vector: [1, 1, 1, 0, 0]

    -> <Vector Search> ->

    Search Results: {...}
    
Args:
	array_field:
		The array field that encoding of the dictionary is trained on
	array:
		The array to encode into vectors
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
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "array": array,
            "array_field": array_field,
            "sum_fields": sum_fields,
            "search_fields": fields,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "asc": asc,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/search_with_array".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)
