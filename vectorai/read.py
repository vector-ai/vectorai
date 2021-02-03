"""Reads Operations designed for python
"""
import io
import base64
import requests
import random
import pandas as pd
import time
import warnings
from typing import List, Dict, Union, Any
from .api.read import ViReadAPIClient
from .utils import UtilsMixin
from .doc_utils import DocUtilsMixin
from .errors import MissingFieldWarning
class ViReadClient(ViReadAPIClient, UtilsMixin, DocUtilsMixin):
    def __init__(self, username: str, api_key: str, url: str="https://api.vctr.ai"):
        self.username = username
        self.api_key = api_key
        self.url = url

    def random_aggregation_query(
        self, collection_name: str, groupby: int = 1, metrics: int = 1
    ):
        """
        Generates a random filter query.

        Args:
            collection_name:
                name of collection
            groupby:
                The number of groupbys to randomly generate
            metrics:
                The number of metrics to randomly generate

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.random_aggregation_query(collection_name, groupby=1, metrics=1)
        """
        schema = self.collection_schema(collection_name)
        full_aggregation_query = {"groupby": [], "metrics": []}
        for s in schema:
            if schema[s] == "text":
                full_aggregation_query["groupby"].append(
                    {"name": s, "field": s, "agg": "texts"}
                )
            elif schema[s] == "numeric":
                full_aggregation_query["metrics"].append(
                    {"name": s, "field": s, "agg": "avg"}
                )
        return {
            "groupby": random.sample(full_aggregation_query["groupby"], groupby),
            "metrics": random.sample(full_aggregation_query["metrics"], metrics),
        }

    def search(self,
        collection_name: str, 
        vector: List,
        field: List,
	filters: List=[],
        approx: int = 0,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
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
	filters:
		Filters for search
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
                
        search_fields ={}
        if isinstance(field, str):
            advanced_search_query = {
                field.replace('_vector_', ''): {'vector': vector, 'fields': [field]}
            }
        else:
            advanced_search_query = {
                field[0].replace('_vector_', ''): {'vector': vector, 'fields': field}
            }
        return self.advanced_search(
            collection_name=collection_name,
            multivector_query=advanced_search_query,
	    filters=filters,
            approx=approx,
            sum_fields=sum_fields,
            metric=metric,
            min_score=min_score,
            page=page,
            page_size=page_size,
            include_vector=include_vector,
            include_count=include_count,
            asc=asc
        )

    def random_filter_query(
        self, collection_name: str, text_filters: int = 1, numeric_filters: int = 0
    ):
        """
        Generates a random filter query.

        Args:
            collection_name:
                name of collection
            text_filters:
                The number of text filters to randomly generate
            numeric_filters:
                The number of numeric filters to randomly generate

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.random_filter_query(collection_name, text_filters=1, numeric_filters=0)
        """
        schema = self.collection_schema(collection_name)
        facets = self.facets(collection_name)
        full_filter_query = {"text": [], "numeric": []}
        for f, t in schema.items():
            if t == "text":
                if isinstance(facets[f], list):
                    full_filter_query["text"].append(
                        {
                            "field": f,
                            "filter_type": "text",
                            "condition_value": random.sample(facets[f], 1)[0][f],
                            "condition": "==",
                        }
                    )
            elif t == "numeric":
                if isinstance(facets[f], dict):
                    full_filter_query["numeric"].append(
                        {
                            "field": f,
                            "filter_type": "date",
                            "condition_value": (facets[f]["max"] - facets[f]["min"])
                            / 2,
                            "condition": ">=",
                        }
                    )
        return random.sample(full_filter_query["text"], text_filters) + random.sample(
            full_filter_query["numeric"], numeric_filters
        )

    def head(
        self, collection_name: str, page_size: int = 5, return_as_pandas_df: bool = True
    ):
        """
        The main Vi client with most of the available read and write methods available to it.

        Args:
            collection_name:
                The name of your collection
            page_size:
                The number of results to return
            return_as_pandas_df:
                If True, return as a pandas DataFrame rather than a JSON.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.head(collection_name, page_size=10)
        """
        response = requests.get(
            url="{}/collection/retrieve_documents".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "page_size": page_size,
            },
        ).json()
        if "documents" in response.keys():
            response = response["documents"]
        if return_as_pandas_df:
            return pd.DataFrame.from_records(response)
        else:
            return response

    def retrieve_all_documents(
        self,
        collection_name: str,
        sort_by: List = [],
        asc: bool = True,
        include_vector: bool = True,
        include_fields: List = [],
        retrieve_chunk_size: int=1000
    ):
        """
        Retrieve all documents in a given collection. We recommend specifying specific fields to extract
        as otherwise this function may take a long time to run.

        Args:
            collection_name:
                Name of collection.
            sort_by:
                Select the fields by which to sort by.
            asc:
                If true, returns in ascending order of what is sort.
            include_vector:
                If true, includes _vector_ fields to return them.
            include_fields:
                Adjust which fields are returned.
            retrieve_chunk_size:
                The number of documents to retrieve per request.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> all_documents = vi_client.retrieve_all_documents(collection_name)
        """
        num_of_docs = self.collection_stats(collection_name)['number_of_documents']
        with self.progress_bar(list(range(int(num_of_docs/ retrieve_chunk_size)))) as pbar:
            d = self.retrieve_documents(
                collection_name, retrieve_chunk_size, sort=sort_by, asc=asc, include_vector=include_vector, 
                include_fields=include_fields
            )
            all_docs = d["documents"]
            pbar.update(1)
            while len(d["documents"]) > 0:
                d = self.retrieve_documents(
                    collection_name,
                    retrieve_chunk_size,
                    d["cursor"],
                    sort=sort_by,
                    asc=asc,
                    include_vector=include_vector,
                    include_fields=include_fields
                )
                all_docs += d["documents"]
                pbar.update(1)
        return all_docs

    def wait_till_jobs_complete(self, collection_name: str, job_id: str, job_name: str):
        """
        Wait until a specific job is complete.

        Args:
            collection_name:
                Name of collection.
            job_id: 
                ID of the job.
            job_name:
                Name of the job.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> job = vi_client.dimensionality_reduction_job('nba_season_per_36_stats_demo', vector_field='season_vector_', n_components=2)
            >>> vi_client.wait_till_jobs_complete('nba_season_per_36_stats_demo', **job)

        """
        status = self.job_status(collection_name, job_id, job_name)
        while (
            status["status"] == "Running"
            or status["status"] == "Started"
            or status["status"] == "NotStarted"
        ):
            status = self.job_status(collection_name, job_id, job_name)
            time.sleep(15)
        print(status)
        return "Done"

    def check_schema(self, collection_name: str, document: Dict=None):
        """
        Check the schema of a given collection.

        Args:
            collection_name:
                Name of collection.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.check_schema(collection_name)
        """
        if document is None:
            document = self.retrieve_documents(collection_name, page_size=1)
        self._check_schema(document)

    def _check_schema(
        self,
        document: Dict,
        is_missing_vector_field=True,
        is_missing_id_field=True,
        is_nested=False
    ):
        """
        Check if there is a _vector_ field and an _id field.

        Args:
            document:
                A JSON file/python dictionary
            is_missing_vector_field:
                DO NOT CHANGE. A tracker to return if the dictionary is missing a vector field
            is_nested:
                DO NOT CHANGE. Returns True if is a nested. Used internally for recursive functionality.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> doc = {'items': {'chicken': 'fried'}, 'food_vector_': [0, 1, 2]}
            >>> vi_client._check_schema(doc)
        """
        VECTOR_FIELD_NAME = "_vector_"
        IS_VECTOR_FIELD_MISSING = True
        IS_ID_FIELD_MISSING = True
        for field, value in document.items():
            if field == '_id':
                IS_ID_FIELD_MISSING = False
            if isinstance(value, dict):
                IS_ID_FIELD_MISSING, IS_VECTOR_FIELD_MISSING = self._check_schema(
                    document[field],
                    is_missing_vector_field=IS_VECTOR_FIELD_MISSING,
                    is_missing_id_field=IS_ID_FIELD_MISSING,
                    is_nested=True
                )
            if "_vectors_" in field:
                warnings.warn(
                    "Rename " + field + "to " + field.replace('_vectors_', '_vector_')
                , MissingFieldWarning)
        
        for field in document.keys():
            if VECTOR_FIELD_NAME in field:
                IS_VECTOR_FIELD_MISSING = False
        
        if not is_nested:
            if IS_VECTOR_FIELD_MISSING:
                warnings.warn(
                    "Potential issue. Cannot find a vector field. Check that the vector field contains _vector_.",
                    MissingFieldWarning
                )
            if IS_ID_FIELD_MISSING:
                warnings.warn(
                    "Missing ID field. Please include an _id field to make inserting easier.",
                    MissingFieldWarning
                )
        return IS_ID_FIELD_MISSING, IS_VECTOR_FIELD_MISSING

    def list_collections(self) -> List[str]:
        """
        List Collections

        Args:
            username:
		        Username
	        api_key:
		        Api Key, you can request it from request_api_key

        Returns:
            List of collections

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> doc = {'items': {'chicken': 'fried'}, 'food_vector_': [0, 1, 2]}
            >>> vi_client._check_schema(doc)
        """
        return sorted(self._list_collections())
    
    def search_collections(self, keyword: str) -> List[str]:
        """
            Performs keyword matching in collections.
            Args:
                keyword: Matches based on keywords
            Returns: 
                List of collection names
            Example: 
                >>> from vectorai import ViClient 
                >>> vi_client = ViClient()
                >>> vi_client.search_collections('example')
        """
        return [x for x in self.list_collections() if keyword.lower() in x]


    def random_recommendation(self,
        collection_name: str, 
        field: str,
        seed=None,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=0,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        approx: int=0,
        hundred_scale=True,
        asc:bool=False):
        """
        Recommend by random ID using vector search
        document_id:
            ID of a document
        collection_name:
            Name of Collection
        field:
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
        random_id = self.random_documents(collection_name, page_size=1, seed=seed, 
        include_fields=['_id'])['documents'][0]['_id']
        return self.search_by_id(collection_name, document_id=random_id, field=field,
        approx=approx, sum_fields=sum_fields, page_size=page_size, page=page, metric=metric, min_score=min_score,
        include_vector=include_vector, include_count=include_count, hundred_scale=hundred_scale,
        asc=asc)

    def create_filter_query(self, collection_name: str, field: str, filter_type: str, filter_values: Union[List[str], str]=None):
        """
            Filter type can be one of contains/exact_match/categories/exists/insert_date/numeric_range
            Filter types can be one of:
            contains: Field must contain this specific string. Not case sensitive.
            exact_match: Field must have an exact match 
            categories: Matches entire field
            exists: If field exists in document 
            >= / > / < / <= : Larger than or equal to / Larger than / Smaller than / Smaller than or equal to
            These, however, can only be applied on numeric/date values. Check collection_schema.

            Args:
            collection_name: The name of the collection 
            field: The field to filter on 
            filter_type: One of contains/exact_match/categories/>=/>/<=/<.

        """
        if filter_type == 'contains':
            return [{'field' : field, 'filter_type' : 'contains', "condition":"==", "condition_value": filter_values}]
        if filter_type == 'exact_match':
            return [{'field' : field, 'filter_type' : 'exact_match', "condition":"==", "condition_value": filter_values}]
        if filter_type == 'categories':
            return [{'field' : field, 'filter_type' : 'categories', "condition":"==", "condition_value": filter_values}]
        if filter_type == 'exists':
            if filter_values is None or filter_values == '==':
                return [{'field' : field, 'filter_type' : 'exists', "condition":"==", "condition_value":" "}]
            elif filter_values == '!=':
                return [{'field' : field, 'filter_type' : 'exists', "condition":"!=", "condition_value":" "}]
        if filter_type == '<=' or filter_type == '>=' or filter_type == '>' or filter_type == '<' or filter_type == '==':
            if self.collection_schema(collection_name)[field] == 'date':
                return [{'field' : field, 'filter_type' : 'date', "condition":filter_type, "condition_value": filter_values}]
            elif self.collection_schema(collection_name)[field] == 'numeric':
                return [{'field' : field, 'filter_type' : 'numeric', "condition":filter_type, "condition_value":filter_values}]
        else:
            raise ValueError(f"{filter_type} has not been defined. Please choose one of contains/exact_match/exists/categories/>=/<=/>/<.")

    def search_with_filters(self,
        collection_name: str, 
        vector: List,
        field: List,
        filters: List=[],
        approx: int = 0,
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False,
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
        search_fields ={}
        if isinstance(field, str):
            advanced_search_query = {
                field.replace('_vector_', ''): {'vector': vector, 'fields': [field]}
            }
        else:
            advanced_search_query = {
                field[0].replace('_vector_', ''): {'vector': vector, 'fields': field}
            }
        return self.advanced_search(
            collection_name=collection_name,
            multivector_query=advanced_search_query,
            approx=approx,
            sum_fields=sum_fields,
            filters=filters,
            metric=metric,
            min_score=min_score,
            page=page,
            page_size=page_size,
            include_vector=include_vector,
            include_count=include_count,
            asc=asc
        )
    
    def hybrid_search_with_filters(
        self,
        collection_name: str,
        text: str,
        vector: List,
        fields: List,
        text_fields: List,
        filters: List=[],
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        traditional_weight=0.075,
        page: int = 1,
        page_size: int = 10,
        include_vector:bool=False,
        include_count:bool=True,
        asc:bool=False
    ):
        """
Search a text field with vector and text using Vector Search and Traditional Search

Vector similarity search + Traditional Fuzzy Search with text and vector.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Hybrid search with filters also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
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
        query = {
            fields[0]: {'vector': vector, 'fields': fields}
        }
        return self.advanced_hybrid_search(
            collection_name=collection_name,
            text=text,
            multivector_query=query,
            text_fields=text_fields,
            sum_fields=sum_fields,
            facets=[],
            filters=filters,
            metric=metric,
            min_score=min_score,
            page=page,
            page_size=page_size,
            include_vector=False,
            include_count=True,
            include_facets=False,
            asc=False
        )
