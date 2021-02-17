import io
import base64
import requests
from typing import Dict, List
from .utils import retry, return_curl_or_response

class ViSearchClient:
    """
    Search and Advanced Search Operations
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

    @retry()
    def _search(
        self,
        collection_name: str,
        vector: List,
        fields: List,
        approx: int = 0,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Vector Similarity Search. Search a vector field with a vector, a.k.a Nearest Neighbors Search

Enables machine learning search with vector search. Search with a vector for the most similar vectors.

For example: Search with a person's characteristics, who are the most similar (querying the "persons_characteristics_vector" field)::

    Query person's characteristics as a vector: 
    [180, 40, 70] representing [height, age, weight]

    Search Results:
    [
        {"name": Adam Levine, "persons_characteristics_vector" : [180, 56, 71]},
        {"name": Brad Pitt, "persons_characteristics_vector" : [180, 56, 65]},
    ...]

Args:
	vector:
		Vector, a list/array of floats that represents a piece of data.
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
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "vector": vector,
            "search_fields": fields,
            "approx" : approx,
            "sum_fields": sum_fields,
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
            url="{}/collection/search".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def hybrid_search(
        self,
        collection_name: str,
        text: str,
        vector: List,
        fields: List,
        text_fields: List,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score: float=None,
        traditional_weight=0.075,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Search a text field with vector and text using Vector Search and Traditional Search

Vector similarity search + Traditional Fuzzy Search with text and vector.
    
Args:
	text:
		Text Search Query (not encoded as vector)
	vector:
		Vector, a list/array of floats that represents a piece of data.
	text_fields:
		Text fields to search against
	traditional_weight:
		Multiplier of traditional search. A value of 0.025~0.1 is good.
	fuzzy:
		Fuzziness of the search. A value of 1-3 is good.
	join:
		Whether to consider cases where there is a space in the word. E.g. Go Pro vs GoPro.
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
            "text": text,
            "vector": vector,
            "search_fields": fields,
            "text_fields": text_fields,
            "sum_fields": sum_fields,
            "metric": metric,
            "min_score": min_score,
            "traditional_weight": traditional_weight,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "asc": asc,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/hybrid_search".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_by_id(
        self,
        collection_name: str,
        document_id: str,
        field: str,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=0,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        approx: int=0,
        hundred_scale: bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Single Product Recommendations (Search by an id)

Recommendation by retrieving the vector from the specified id's document. Then performing a search with that vector.
    
Args:
	document_id:
		ID of a document
	collection_name:
		Name of Collection
	search_field:
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
    return_curl:
        Return the CURL statement relevant to the Python requests
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document_id": document_id,
            "search_field": field,
            "sum_fields": sum_fields,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "asc": asc,
            "approx": approx,
            "hundred_scale": hundred_scale
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/search_by_id".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_by_ids(
        self,
        collection_name: str,
        document_ids: List,
        field: str,
        vector_operation: str = "mean",
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=0,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Multi Product Recommendations (Search by ids)

Recommendation by retrieving the vectors from the specified list of ids documents. Then performing a search with an aggregated vector that is the sum (depends on vector_operation) of those vectors.
    
Args:
	document_ids:
		IDs of documents
	vector_operation:
		Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
	collection_name:
		Name of Collection
	search_field:
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
            "document_ids": document_ids,
            "search_field": field,
            "vector_operation": vector_operation,
            "sum_fields": sum_fields,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "asc": asc
        }
        response = requests.get(
            url="{}/collection/search_by_ids".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_by_positive_negative_ids(
        self,
        collection_name: str,
        positive_document_ids: List,
        negative_document_ids: List,
        field: str,
        vector_operation: str = "mean",
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=0,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Multi Product Recommendations with Likes and Dislikes (Search by ids)

Recommendation by retrieving the vectors from the specified list of positive and negative ids documents. Then performing a search with an aggregated vector that is the sum (depends on vector_operation) of positive id vectors minus the negative id vectors.
    
Args:
	positive_document_ids:
		Positive Document IDs to get recommendations for, and the weightings of each document
	negative_document_ids:
		Negative Document IDs to get recommendations for, and the weightings of each document
	vector_operation:
		Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
	collection_name:
		Name of Collection
	search_field:
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
            "positive_document_ids": positive_document_ids,
            "negative_document_ids": negative_document_ids,
            "search_field": field,
            "vector_operation": vector_operation,
            "sum_fields": sum_fields,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "asc": asc
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/search_by_positive_negative_ids".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def search_with_positive_negative_ids_as_history(
        self,
        collection_name: str,
        vector: List,
        positive_document_ids: List,
        negative_document_ids: List,
        field: str,
        vector_operation: str = "mean",
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=0,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Multi Product Recommendations with Likes and Dislikes (Search by ids)

Search by retrieving the vectors from the specified list of positive and negative ids documents. Then performing a search with search query vector and aggregated vector, that is the sum (depends on vector_operation) of positive id vectors minus the negative id vectors.
    
Args:
	vector:
		Vector, a list/array of floats that represents a piece of data.
	positive_document_ids:
		Positive Document IDs to get recommendations for, and the weightings of each document
	negative_document_ids:
		Negative Document IDs to get recommendations for, and the weightings of each document
	vector_operation:
		Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
	collection_name:
		Name of Collection
	search_field:
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
            "vector": vector,
            "positive_document_ids": positive_document_ids,
            "negative_document_ids": negative_document_ids,
            "search_field": field,
            "vector_operation": vector_operation,
            "sum_fields": sum_fields,
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
            url="{}/collection/search_with_positive_negative_ids_as_history".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def advanced_search(
        self,
        collection_name: str,
        multivector_query: Dict,
        sum_fields: bool = True,
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        approx:int=0,
        return_curl: bool=False,
        **kwargs
    ):
        """
Advanced Vector Similarity Search. Support for multiple vectors, vector weightings, facets and filtering

Advance Vector Similarity Search, enables machine learning search with vector search. Search with a multiple vectors for the most similar documents.

For example: Search with a product image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args:
	collection_name:
		Name of Collection
	multivector_query:
		Query for advance search that allows for multiple vector and field querying
	page:
		Page of the results
	page_size:
		Size of each page of results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	filters:
		Query for filtering the search results
	facets:
		Fields to include in the facets, if [] then all
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	include_facets:
		Include facets in the search results
	hundred_scale:
		Whether to scale up the metric by 100
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)

Example:
    >>> vi_client = ViCollectionClient(username, api_key, collection_name, url)
    >>> advanced_search_query = {
            'text' : {'vector': encode_question("How do I cluster?"), 'fields' : ['function_vector_']}
        }
    >>> vi_client.advanced_search(advanced_search_query)
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "multivector_query": multivector_query,
            "facets": facets,
            "filters": filters,
            "sum_fields": sum_fields,
            "approx" : approx,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "include_facets": include_facets,
            "asc": asc,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/advanced_search".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def advanced_hybrid_search(
        self,
        collection_name: str,
        text: str,
        multivector_query: Dict,
        text_fields: List,
        sum_fields: bool = True,
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Advanced Search a text field with vector and text using Vector Search and Traditional Search

Advanced Vector similarity search + Traditional Fuzzy Search with text and vector.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args:
	collection_name:
		Name of Collection
	page:
		Page of the results
	page_size:
		Size of each page of results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	filters:
		Query for filtering the search results
	facets:
		Fields to include in the facets, if [] then all
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	include_facets:
		Include facets in the search results
	hundred_scale:
		Whether to scale up the metric by 100
	multivector_query:
		Query for advance search that allows for multiple vector and field querying
	text:
		Text Search Query (not encoded as vector)
	text_fields:
		Text fields to search against
	traditional_weight:
		Multiplier of traditional search. A value of 0.025~0.1 is good.
	fuzzy:
		Fuzziness of the search. A value of 1-3 is good.
	join:
		Whether to consider cases where there is a space in the word. E.g. Go Pro vs GoPro.
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""


        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "text": text,
            "multivector_query": multivector_query,
            "text_fields": text_fields,
            "sum_fields": sum_fields,
            "facets": facets,
            "filters": filters,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "include_facets": include_facets,
            "asc": asc,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/advanced_hybrid_search".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def advanced_search_by_id(
        self,
        collection_name: str,
        document_id: str,
        fields: Dict,
        sum_fields: bool = True,
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Advanced Single Product Recommendations (Search by an id).

For example: Search with id of a product in the database, and using the product's image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args:
	collection_name:
		Name of Collection
	page:
		Page of the results
	page_size:
		Size of each page of results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	filters:
		Query for filtering the search results
	facets:
		Fields to include in the facets, if [] then all
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	include_facets:
		Include facets in the search results
	hundred_scale:
		Whether to scale up the metric by 100
	document_id:
		ID of a document
	search_fields:
		Vector fields to search against, and the weightings for them.
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)

Example:
    >>> filter_query = [
            {'field': 'field_name',
            'filter_type': 'text',
            'condition_value': 'monkl',
            'condition': '=='}
        ]
    >>> results = client.advanced_search_by_id(document_id=client.random_documents()['documents'][0]['_id'], 
    fields={'image_url_field_flattened_vector_':1}, filters=filter_query)

"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document_id": document_id,
            "search_fields": fields,
            "sum_fields": sum_fields,
            "facets": facets,
            "filters": filters,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "include_facets": include_facets,
            "asc": asc
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/advanced_search_by_id".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def advanced_search_by_ids(
        self,
        collection_name: str,
        document_ids: Dict,
        fields: Dict,
        vector_operation: str = "mean",
        sum_fields: bool = True,
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Advanced Multi Product Recommendations (Search by ids).

For example: Search with multiple ids of products in the database, and using the product's image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

You can also give weightings of on each product as well e.g. product ID-A weights 100% whilst product ID-B 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args:
	collection_name:
		Name of Collection
	page:
		Page of the results
	page_size:
		Size of each page of results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	filters:
		Query for filtering the search results
	facets:
		Fields to include in the facets, if [] then all
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	include_facets:
		Include facets in the search results
	hundred_scale:
		Whether to scale up the metric by 100
	document_ids:
		Document IDs to get recommendations for, and the weightings of each document
	search_fields:
		Vector fields to search against, and the weightings for them.
	vector_operation:
		Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        params = {
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "document_ids": document_ids,
                "search_fields": fields,
                "vector_operation": vector_operation,
                "sum_fields": sum_fields,
                "facets": facets,
                "filters": filters,
                "metric": metric,
                "min_score": min_score,
                "page": page,
                "page_size": page_size,
                "include_vector": include_vector,
                "include_count": include_count,
                "include_facets": include_facets,
                "asc": asc
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/advanced_search_by_ids".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def advanced_search_by_positive_negative_ids(
        self,
        collection_name: str,
        positive_document_ids: Dict,
        negative_document_ids: Dict,
        fields: Dict,
        vector_operation: str = "mean",
        sum_fields: bool = True,
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Advanced Multi Product Recommendations with likes and dislikes (Search by ids).

For example: Search with multiple ids of liked and dislike products in the database. Then using the product's image and description vectors to find the most similar products by what it looks like and what its described to do against the positives and most disimilar products for the negatives.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

You can also give weightings of on each product as well e.g. product ID-A weights 100% whilst product ID-B 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args:
	collection_name:
		Name of Collection
	page:
		Page of the results
	page_size:
		Size of each page of results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	filters:
		Query for filtering the search results
	facets:
		Fields to include in the facets, if [] then all
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	include_facets:
		Include facets in the search results
	hundred_scale:
		Whether to scale up the metric by 100
	positive_document_ids:
		Positive Document IDs to get recommendations for, and the weightings of each document
	negative_document_ids:
		Negative Document IDs to get recommendations for, and the weightings of each document
	search_fields:
		Vector fields to search against, and the weightings for them.
	vector_operation:
		Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        params = {
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "positive_document_ids": positive_document_ids,
                "negative_document_ids": negative_document_ids,
                "search_fields": fields,
                "vector_operation": vector_operation,
                "sum_fields": sum_fields,
                "facets": facets,
                "filters": filters,
                "metric": metric,
                "min_score": min_score,
                "page": page,
                "page_size": page_size,
                "include_vector": include_vector,
                "include_count": include_count,
                "include_facets": include_facets,
                "asc": asc,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/advanced_search_by_positive_negative_ids".format(
                self.url
            ),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def advanced_search_with_positive_negative_ids_as_history(
        self,
        collection_name: str,
        vector:List,
        positive_document_ids: Dict,
        negative_document_ids: Dict,
        fields: Dict,
        vector_operation: str = "mean",
        sum_fields: bool = True,
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Advanced Search with Likes and Dislikes as history

For example: Vector search of a query vector with multiple ids of liked and dislike products in the database. Then using the product's image and description vectors to find the most similar products by what it looks like and what its described to do against the positives and most disimilar products for the negatives.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

You can also give weightings of on each product as well e.g. product ID-A weights 100% whilst product ID-B 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args:
	collection_name:
		Name of Collection
	page:
		Page of the results
	page_size:
		Size of each page of results
	approx:
		Used for approximate search
	sum_fields:
		Whether to sum the multiple vectors similarity search score as 1 or seperate
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	filters:
		Query for filtering the search results
	facets:
		Fields to include in the facets, if [] then all
	min_score:
		Minimum score for similarity metric
	include_vector:
		Include vectors in the search results
	include_count:
		Include count in the search results
	include_facets:
		Include facets in the search results
	hundred_scale:
		Whether to scale up the metric by 100
	positive_document_ids:
		Positive Document IDs to get recommendations for, and the weightings of each document
	negative_document_ids:
		Negative Document IDs to get recommendations for, and the weightings of each document
	search_fields:
		Vector fields to search against, and the weightings for them.
	vector_operation:
		Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
	vector:
		Vector, a list/array of floats that represents a piece of data
    asc:
        Whether to sort the score by ascending order (default is false, for getting most similar results)
"""
        params = {
                "username": self.username,
                "api_key": self.api_key,
                "vector": vector,
                "collection_name": collection_name,
                "positive_document_ids": positive_document_ids,
                "negative_document_ids": negative_document_ids,
                "search_fields": fields,
                "vector_operation": vector_operation,
                "sum_fields": sum_fields,
                "facets": facets,
                "filters": filters,
                "metric": metric,
                "min_score": min_score,
                "page": page,
                "page_size": page_size,
                "include_vector": include_vector,
                "include_count": include_count,
                "include_facets": include_facets,
                "asc": asc,
        } 
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/advanced_search_with_positive_negative_ids_as_history".format(
                self.url
            ),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def chunk_search(self, 
        collection_name:  str, 
        vector: List, 
        search_fields: list, 
        chunk_scoring: str="max",
        facets: List = [],
        filters: List = [],
        metric: str = "cosine",
        sum_fields: bool=True,
        approx: int=0,
        min_score=None,
        page: int = 1,
        page_size: int = 20,
        include_vector:bool=False,
        include_count:bool=True,
        include_facets:bool=False,
        asc:bool=False,
        return_curl: bool=False,
        **kwargs):
        """
            Chunk search functionality
            Args:
                collection_name: Name of collection
                vector: A list of values 
                Search_fields: A list of fields to search
                chunk_scoring: How each chunk should be scored
                approx: How many approximate neighbors to go through
        """
        params = {
            "username" : self.username,
            "api_key" : self.api_key,
            "collection_name": collection_name,
            "vector" : vector,
            "chunk_scoring": chunk_scoring,
            "search_fields" : search_fields,
            "sum_fields": sum_fields,
            "approx": approx,
            "facets": facets,
            "filters": filters,
            "metric": metric,
            "min_score": min_score,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
            "include_count": include_count,
            "include_facets": include_facets,
            "asc": asc
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/chunk_search".format(
                self.url
            ),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)
