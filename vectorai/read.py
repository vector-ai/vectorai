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

class ViReadClient(ViReadAPIClient, UtilsMixin, DocUtilsMixin):
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

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
        sum_fields: bool = True,
        metric: str = "cosine",
        min_score=None,
        page: int = 1,
        page_size: int = 10,
        include_vector=False,
        include_count=True):

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
"""                
                
                search_fields ={}
                advanced_search_query = {
                    field.replace('_vector_', ''): {'vector': vector, 'fields': [field]}
                }
                return self.advanced_search(
                    collection_name=collection_name,
                    multivector_query=advanced_search_query,
                    sum_fields=sum_fields,
                    metric=metric,
                    min_score=min_score,
                    page=page,
                    page_size=page_size,
                    include_vector=include_vector,
                    include_count=include_count
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
        include_fields: List = []
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

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> all_documents = vi_client.retrieve_all_documents(collection_name)
        """
        d = self.retrieve_documents(
            collection_name, 1000, sort=sort_by, asc=asc, include_vector=include_vector, 
            include_fields=include_fields
        )
        all_docs = d["documents"]
        while len(d["documents"]) > 0:
            d = self.retrieve_documents(
                collection_name,
                1000,
                d["cursor"],
                sort=sort_by,
                asc=asc,
                include_vector=include_vector,
                include_fields=include_fields
            )
            all_docs += d["documents"]
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

    def check_schema(self, collection_name: str):
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
        document = self.retrieve_documents(collection_name, page_size=1)
        self._check_schema(document)

    def _check_schema(
        self,
        document: Dict,
        schema={},
        is_missing_vector_field=True,
        return_schema: bool = False,
    ):
        """
        Check the schema of a given collection.

        Args:
            document:
                A JSON file/python dictionary
            schema:
                A schema tracker if the schema wants to be returned.
            is_missing_vector_field:
                A tracker to return if the dictionary is missing a vector field
            return_schema:
                A boolean representation if you want the schema returned.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> doc = {'items': {'chicken': 'fried'}, 'food_vector_': [0, 1, 2]}
            >>> vi_client._check_schema(doc)
        """
        VECTOR_FIELD_NAME = "_vector_"
        MISSING_VECTOR_FIELD = True
        for field in document.keys():
            if "_vectors_" in field:
                warnings.warn(
                    f"Rename {field} to contain {field.replace('_vectors_', '_vector_')}"
                )
            if VECTOR_FIELD_NAME in field:
                MISSING_VECTOR_FIELD = False
            value = self.get_field(field, document)
            schema[field] = {}
            if isinstance(value, dict):
                MISSING_VECTOR_FIELD = self._check_schema(
                    document[field],
                    schema=schema[field],
                    is_missing_vector_field=MISSING_VECTOR_FIELD,
                    return_schema=False,
                )

        if MISSING_VECTOR_FIELD:
            warnings.warn(
                "Potential issue. Cannot find a vector field. Check that the vector field contains _vector_."
            )
        if return_schema:
            return MISSING_VECTOR_FIELD, schema
        return MISSING_VECTOR_FIELD

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
