import requests
import random
from typing import Dict, List
from .audio import ViAudioClient
from .image import ViImageClient
from .text import ViTextClient
from .cluster import ViClusterClient
from .search import ViSearchClient
from .dimensionality_reduction import ViDimensionalityReductionClient
from .array_dict_vectorizer import ViArrayDictClient
from .utils import retry, return_curl_or_response

class ViReadAPIClient(
    ViSearchClient,
    ViTextClient,
    ViAudioClient,
    ViImageClient,
    ViClusterClient,
    ViDimensionalityReductionClient,
    ViArrayDictClient
):
    """
    Read Operations
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"
            
    @retry()
    def _list_collections(self, return_curl: bool=False, **kwargs):
        """
Lists all the collections in a project

Retrieve a list all the created collections.
    
Args:
	username:
		Username
	api_key:
		Api Key, you can request it from request_api_key
"""
        params = {
            "username": self.username, 
            "api_key": self.api_key
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/project/list_collections".format(self.url),
            params=params,
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def collection_stats(self, collection_name: str, return_curl: bool=False, **kwargs):
        """
Retrieves stats about a collection

Stats include: size, searches, number of documents, etc.
    
Args:
	collection_name:
		Name of Collection
"""

        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/project/collection_stats".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def collection_schema(self, collection_name: str, return_curl: bool=False, **kwargs):
        """
Retrieves the schema of a collection

The schema of a collection can include types of: text, numeric, date, bool, etc.
    
Args:
	collection_name:
		Name of Collection
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name
        }
        params.update(kwargs)

        response = requests.get(
            url="{}/project/collection_schema".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def id(self, collection_name: str, document_id: str, include_vector: bool = True, return_curl: bool=False, **kwargs):
        """
Look up a document by its id
    
Args:
	document_id:
		ID of a document
	include_vector:
		Include vectors in the search results
	collection_name:
		Name of Collection
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document_id": document_id,
            "include_vector": include_vector,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/id".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def bulk_id(self, collection_name: str, document_ids: List[str], return_curl: bool=False, **kwargs):
        """
Look up multiple document by their ids
    
Args:
	document_ids:
		IDs of documents
	include_vector:
		Include vectors in the search results
	collection_name:
		Name of Collection
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document_ids": document_ids,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/bulk_id".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def retrieve_documents(
        self,
        collection_name: str,
        page_size: int = 20,
        cursor: str = None,
        sort: List = [],
        asc: bool = True,
        include_vector: bool = True,
        include_fields: List = [],
        return_curl: bool=False,
        **kwargs
    ):
        """
Retrieve some documents

Cursor is provided to retrieve even more documents. Loop through it to retrieve all documents in the database.
    
Args:
	include_fields:
		Fields to include in the document, if empty list [] then all is returned
	cursor:
		Cursor to paginate the document retrieval
	page_size:
		Size of each page of results
	sort:
		Fields to sort the documents by
	asc:
		Whether to sort results by ascending or descending order
	include_vector:
		Include vectors in the search results
	collection_name:
		Name of Collection
"""
        q_params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "include_fields": include_fields,
            "page_size": page_size,
            "cursor": cursor,
            "asc": asc,
            "include_vector": include_vector,
        }
        if sort:
            q_params["sort"] = sort
        q_params.update(kwargs)
        response = requests.get(
            url="{}/collection/retrieve_documents".format(self.url), params=q_params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def random_documents(
        self,
        collection_name: str,
        page_size: int = 20,
        seed: int = None,
        include_vector: bool = True,
        include_fields: list = [],
        return_curl: bool=False,
        **kwargs
    ):
        """
Retrieve some documents randomly

Mainly for testing purposes.
    
Args:
	seed:
		Random Seed for retrieving random documents.
	page_size:
		Size of each page of results
	include_vector:
		Include vectors in the search results
	collection_name:
		Name of Collection
    return_curl:
        Return CURL statement
"""
        if seed is None:
            seed = random.randint(0, 9999)
        q_params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "page_size": page_size,
            "seed": seed,
            "include_vector": include_vector,
            "include_fields": include_fields
        }
        q_params.update(kwargs)

        response = requests.get(
            url="{}/collection/random_documents".format(self.url), params=q_params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def id_lookup_joined(self, join_query: dict, doc_id:str, return_curl: bool=False, **kwargs):
        """
Look up a document by its id with joins
    
Args:
	join_query:
		.
	doc_id:
		ID of a Document
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "join_query": join_query,
            "doc_id" : doc_id,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/id_lookup_joined".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)
        
    @retry()
    def aggregate(
        self,
        collection_name: str,
        aggregation_query: Dict,
        page:int=1,
        page_size:int=10,
        asc:bool=False,
        flatten:bool=True,
        return_curl: bool=False,
        **kwargs
    ):
        """
Aggregate a collection

Aggregation/Groupby of a collection using an aggregation query. 
The aggregation query is a json body that follows the schema of:: 

    {
        "groupby" : [
            {"name": <nickname/alias>, "field": <field in the collection>, "agg": "category"},
            {"name": <another_nickname/alias>, "field": <another groupby field in the collection>, "agg": "category"}
        ], 
        "metrics" : [
            {"name": <nickname/alias>, "field": <numeric field in the collection>, "agg": "avg"}
        ]
    }

- "groupby" is the fields you want to split the data into. These are the available groupby types:

    - category" : groupby a field that is a category
- "metrics" is the fields you want to metrics you want to calculate in each of those. These are the available metric types: every aggregation includes a frequency metric:

    - average", "max", "min", "sum", "cardinality"
    
Args:
	collection_name:
		Name of Collection
	aggregation_query:
		Aggregation query to aggregate data
	page_size:
		Size of each page of results
	page:
		Page of the results
	asc:
		Whether to sort results by ascending or descending order
    flatten:
        Whether to flatten the aggregated results into a list of dictionarys or dictionary of lists.
    return_curl:
        Return the CURL statement
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "aggregation_query": aggregation_query,
            "page": page,
            "page_size": page_size,
            "asc": asc,
            "flatten" : flatten
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/aggregate".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def facets(
        self,
        collection_name: str,
        fields: List[str] = [],
        page: int = 1,
        page_size: int = 20,
        asc: bool = False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Retrieve the facets of a collection

Takes a high level aggregation of every field in a collection. This is used in advance search to help create the filter bar for search.
    
Args:
	facets_fields:
		Fields to include in the facets, if [] then all
	date_interval:
		Interval for date facets
	page_size:
		Size of facet page
	page:
		Page of the results
	asc:
		Whether to sort results by ascending or descending order
	collection_name:
		Name of Collection
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "facets_fields" : fields,
            "collection_name": collection_name,
            "page": page,
            "page_size": page_size,
            "asc": asc,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/facets".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def filters(
        self,
        collection_name: str,
        filters: List,
        page=1,
        page_size=10,
        include_vector: bool = False,
        return_curl: bool=False,
        **kwargs
    ):
        """
Filters a collection

Filter is used to retrieve documents that match the conditions set in a filter query. This is used in advance search to filter the documents that are searched.

The filters query is a json body that follows the schema of::

    [
        {'field' : <field to filter>, 'filter_type' : <type of filter>, "condition":"==", "condition_value":"america"},
        {'field' : <field to filter>, 'filter_type' : <type of filter>, "condition":">=", "condition_value":90},
    ]

These are the available filter_type types::

    1. "contains": for filtering documents that contains a string.
            {'field' : 'category', 'filter_type' : 'contains', "condition":"==", "condition_value": "bluetoo"]}
    2. "exact_match"/"category": for filtering documents that matches a string or list of strings exactly.
            {'field' : 'category', 'filter_type' : 'categories', "condition":"==", "condition_value": "tv"]}
    3. "categories": for filtering documents that contains any of a category from a list of categories.
            {'field' : 'category', 'filter_type' : 'categories', "condition":"==", "condition_value": ["tv", "smart", "bluetooth_compatible"]}
    4. "exists": for filtering documents that contains a field.
            {'field' : 'purchased', 'filter_type' : 'exists', "condition":">=", "condition_value":" "}
    5. "date": for filtering date by date range.
            {'field' : 'insert_date_', 'filter_type' : 'date', "condition":">=", "condition_value":"2020-01-01"}
    6. "numeric": for filtering by numeric range. 
            {'field' : 'price', 'filter_type' : 'date', "condition":">=", "condition_value":90}

These are the available conditions:
 
    "==", "!=", ">=", ">", "<", "<="
    
Args:
	collection_name:
		Name of Collection
	filters:
		Query for filtering the search results
	page:
		Page of the results
	page_size:
		Size of each page of results
	asc:
		Whether to sort results by ascending or descending order
	include_vector:
		Include vectors in the search results
    return_curl:
        Returns Curl statement for debugging
"""
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "filters": filters,
            "page": page,
            "page_size": page_size,
            "include_vector": include_vector,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/filters".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def job_status(self, collection_name: str, job_id: str, job_name: str, return_curl: bool=False, **kwargs):
        """
Get status of a job. Whether its starting, running, failed or finished.
    
Args:
	job_id:
		.
	job_name:
		.
	collection_name:
		Name of Collection
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "job_id": job_id,
            "job_name": job_name,
        }
        response = requests.get(
            url="{}/collection/jobs/job_status".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def list_jobs(self, collection_name: str, return_curl: bool=False, **kwargs):
        """
Get history of jobs

List and get a history of all the jobs and its job_id, parameters, start time, etc.
    
Args:
	collection_name:
		Name of Collection
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/jobs/list_jobs".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def bulk_missing_id(self, collection_name: str, document_ids: List[str], return_curl: bool=False, **kwargs):
        """
            Return IDs that are not in a collection.
        """
        params = {
            "username" : self.username,
            "api_key" : self.api_key,
            "collection_name": collection_name,
            "document_ids" : document_ids
        }
        params.update(kwargs)
        response = requests.post('{}/collection/bulk_missing_id'.format(self.url), 
        json=params)
        return return_curl_or_response(response, 'json', return_curl=return_curl)
    
    @retry()
    def random_documents_with_filters(self, collection_name: str,
    seed: int=None, include_fields: List[str]=[], page_size: int=20,
    include_vector: bool=False, filters: List[Dict]=[], return_curl: bool=False, **kwargs):
        """
            Random documents with filters.
        """

        if seed is None:
            seed = random.randint(0, 9999)

        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "seed": seed,
            "include_fields": include_fields,
            "page_size": page_size,
            "include_vector": include_vector,
            "filters": filters
        }

        response = requests.post('{}/collection/random_documents_with_filters'.format(self.url), json=params)
        return return_curl_or_response(response, 'json', return_curl=return_curl)

    @retry()
    def vector_health(self, collection_name: str, return_curl: bool=False, **kwargs):
        """Return vector health of a collection
        """
        params = {
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name
        }
        params.update(kwargs)
        response = requests.get("{}/collection/vector_health".format(self.url), params=params)
        return return_curl_or_response(response, 'json', return_curl=return_curl)
        
