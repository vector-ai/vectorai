import io
import base64
import requests
from typing import Dict, List
from .utils import retry

class ViClusterClient:
    """
    Clustering
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"
    
    @retry()
    def clustering_job(
        self,
        collection_name: str,
        vector_field: str,
        n_clusters: int = 0,
        refresh: bool = True,
    ):
        """
Clusters a collection by a vector field

Clusters a collection into groups using unsupervised machine learning. Clusters can then be aggregated to understand whats in them and how vectors are seperating data into different groups.
        
Args:
	vector_field:
		Vector field to perform clustering on
	n_clusters:
		Number of clusters
	refresh:
		Whether to refresh the whole collection and retrain the cluster model
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/jobs/cluster".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "n_clusters": n_clusters,
                "refresh": refresh,
            },
        ).json()

    @retry()
    def cluster_aggregate(
        self,
        collection_name: str,
        aggregation_query: Dict,
        page: int = 1,
        page_size: int = 10,
        asc: bool = False,
        flatten: bool = True,
    ):
        """
Aggregate every cluster in a collection

Takes an aggregation query and gets the aggregate of each cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /cluster.
    
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
"""
        return requests.post(
            url="{}/collection/cluster_aggregate".format(self.url),
            json={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "aggregation_query": aggregation_query,
                "page": page,
                "page_size": page_size,
                "asc": asc,
                "flatten" : flatten
            },
        ).json()

    @retry()
    def cluster_facets(self, collection_name: str, facets_fields: List = [], asc: bool = True,
    page_size: int=1000, page: int=1, date_interval: str="monthly"):
        """
Get Facets in each cluster in a collection

Takes a high level aggregation of every field and every cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /cluster.
    
Args:
	facets_fields:
		Fields to include in the facets, if [] then all
	page_size:
		Size of facet page
	page:
		Page of the results
	asc:
		Whether to sort results by ascending or descending order
	date_interval:
		Interval for date facets
	collection_name:
		Name of Collection
    date_interval:
        Defaults "monthly". Interval for date facets
"""
        return requests.get(
            url="{}/collection/cluster_facets".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "facets_fields": facets_fields,
                "page_size": page_size,
                "page": page,
                "asc": asc,
                "date_interval": date_interval
            },
        ).json()

    @retry()
    def cluster_centroids(self, collection_name: str, vector_field: str):
        """
Returns the cluster centers of a collection by a vector field

Only can be used after a vector field has been clustered with /cluster.
    
Args:
	vector_field:
		Clustered vector field
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/cluster_centroids".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
            },
        ).json()

    @retry()
    def cluster_centroid_documents(
        self,
        collection_name: str,
        vector_field: str,
        metric: str = "cosine",
        include_vector: bool = True,
    ):
        """
Returns the document closest to each cluster center of a collection

Only can be used after a vector field has been clustered with /cluster.
    
Args:
	vector_field:
		Clustered vector field
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	include_vector:
		Include vectors in the search results
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/cluster_centroid_documents".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "metric": metric,
                "include_vector": include_vector,
            },
        ).json()

    @retry()
    def advanced_clustering_job(
        self,
        collection_name: str,
        vector_field: str,
        alias: str='default',
        n_clusters: int = 0,
        n_init: int = 5,
        n_iter: int = 10,
        refresh: bool = True,
    ):
        """
Clusters a collection by a vector field

Clusters a collection into groups using unsupervised machine learning. Clusters can then be aggregated to understand whats in them and how vectors are seperating data into different groups. 
Advanced cluster allows for more parameters to tune and alias to name each differently trained clusters.
        
Args:
	vector_field:
		Vector field to perform clustering on
	alias:
		Alias is used to name a cluster
	n_clusters:
		Number of clusters
	n_iter:
		Number of iterations in each run
	n_init:
		Number of runs to run with different centroid seeds
	refresh:
		Whether to refresh the whole collection and retrain the cluster model
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/jobs/advanced_cluster".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "alias": alias,
                "n_clusters": n_clusters,
                "n_init": n_init,
                "n_iter": n_iter,
                "refresh": refresh,
            },
        ).json()

    @retry()
    def advanced_cluster_aggregate(
        self,
        collection_name: str,
        aggregation_query: Dict,
        vector_field: str,
        alias: str = "default",
        page: int = 1,
        page_size: int = 10,
        asc: bool = False,
        filters: list = [],
        flatten:bool=True,
    ):
        """
Aggregate every cluster in a collection

Takes an aggregation query and gets the aggregate of each cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /advanced_cluster.
    
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
	vector_field:
		Clustered vector field
	alias:
		Alias of a cluster
    flatten:
        Whether to flatten the aggregated results into a list of dictionarys or dictionary of lists.
"""
        return requests.post(
            url="{}/collection/advanced_cluster_aggregate".format(self.url),
            json={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field" : vector_field,
                "aggregation_query": aggregation_query,
                "page": page,
                "page_size": page_size,
                "asc": asc,
                "alias": alias,
                "filters" : filters,
                "flatten" : flatten
            },
        ).json()

    @retry()
    def advanced_cluster_facets(
        self,
        collection_name: str,
        vector_field: str,
        alias: str = "default",
        facets_fields: List = [],
        asc: bool = True,
    ):
        """
Get Facets in each cluster in a collection

Takes a high level aggregation of every field and every cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /advanced_cluster.
    
Args:
	vector_field:
		Clustered vector field
	alias:
		Alias is used to name a cluster
	facets_fields:
		Fields to include in the facets, if [] then all
	page_size:
		Size of facet page
	page:
		Page of the results
	asc:
		Whether to sort results by ascending or descending order
	date_interval:
		Interval for date facets
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/advanced_cluster_facets".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "facets_fields": facets_fields,
                "alias": alias,
            },
        ).json()

    @retry()
    def advanced_cluster_centroids(
        self, collection_name: str, vector_field: str, alias: str = "default"
    ):
        """
Returns the cluster centers of a collection by a vector field

Only can be used after a vector field has been clustered with /advanced_cluster.
    
Args:
	vector_field:
		Clustered vector field
	alias:
		Alias is used to name a cluster
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/advanced_cluster_centroids".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "alias": alias,
            },
        ).json()

    @retry()
    def advanced_cluster_centroid_documents(
        self,
        collection_name: str,
        vector_field: str,
        alias: str = "default",
        metric: str = "cosine",
        include_vector: bool = True,
    ):
        """
Returns the document closest to each cluster center of a collection

Only can be used after a vector field has been clustered with /advanced_cluster.
    
Args:
	vector_field:
		Clustered vector field
	alias:
		Alias is used to name a cluster
	metric:
		Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
	include_vector:
		Include vectors in the search results
	collection_name:
		Name of Collection
"""
        return requests.get(
            url="{}/collection/advanced_cluster_centroid_documents".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": collection_name,
                "vector_field": vector_field,
                "metric": metric,
                "include_vector": include_vector,
                "alias": alias,
            },
        ).json()
