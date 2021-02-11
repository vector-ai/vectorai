import requests
from typing import Dict, List
from .read import ViReadAPIClient
from .utils import retry, return_curl_or_response
from ..errors import APIError, CollectionNameError

class ViWriteAPIClient(ViReadAPIClient):
    """
    Write Operations
    """
    def __init__(self, username, api_key, url=None):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"

    def _typecheck_collection_name(self, collection_name: str):
        ACCEPTABLE_LETTERS = 'abcdefghijklmnopqrstuvwxyz_.'
        for letter in collection_name: 
            if letter not in ACCEPTABLE_LETTERS:
                raise CollectionNameError("Collection names must be lower case A-Z and less than 240 characters")
        if len(collection_name) > 240:
            raise CollectionNameError("Collection names must be lower case A-Z and less than 240 characters")
    
    @retry()
    def create_collection_from_document(self, collection_name: str, document: dict, return_curl: bool=False, **kwargs):
        """
Creates a collection by infering the schema from a document

If you are inserting your own vector use the suffix (ends with)  **"\_vector\_"** for the field name. e.g. "product\_description\_vector\_"
    
Args:
	collection_name:
		Name of Collection
	document:
		A Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
"""
        self._typecheck_collection_name(collection_name)
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document": document,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/project/create_collection_from_document".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def bulk_insert_and_encode(self, collection_name: str, docs: list, models: dict, return_curl: bool=False, **kwargs):
        """
            Client-side encoding of documents to improve speed of inserting. This removes
            the step of retrieving the vectors and can be useful to accelerate the encoding
            process if required.
            Models can be one of 'text', 'audio' or 'image'.
        """
        # For each of the field values in the models, check that the deployed models
        # are in the list below.
        for k, v in models.items():
            assert v in ['text', 'audio', 'image']

        params={
            'username' : self.username,
            'api_key' : self.api_key,
            'collection_name': collection_name,
            'documents' : docs,
            'models' : models
        }
        params.update(kwargs)
        response = requests.post(
            url='{}/collection/bulk_insert_and_encode'.format(self.url), 
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def _create_collection(self, collection_name: str, collection_schema: Dict = {}, return_curl: bool=False, **kwargs):

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "collection_schema": collection_schema,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/project/create_collection".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)


    @retry()
    def _delete_collection(self, collection_name: str, return_curl: bool=False, **kwargs):
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/project/delete_collection".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    # def replicate_collection(self, collection_name: str, new_collection_name: str):
    #     return requests.get(
    #         url="{}/project/replicate_collection".format(self.url),
    #         params={
    #             "username": self.username,
    #             "api_key": self.api_key,
    #             "collection_name": collection_name,
    #             "new_collection_name": collection_name,
    #         },
    #     ).json()

    @retry()
    def bulk_insert(self, collection_name: str, documents: List, insert_date: bool=True, overwrite: bool=True, 
    quick: bool=False, return_curl: bool=False, **kwargs):
        """
Insert multiple documents into a Collection
When inserting the document you can specify your own id for a document by using the field name **"\_id"**. 
For specifying your own vector use the suffix (ends with)  **"\_vector\_"** for the field name.
e.g. "product\_description\_vector\_"
    
Args:
	collection_name:
		Name of Collection
	documents:
		A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
	insert_date:
		Whether to include insert date as a field 'insert_date_'.
	overwrite:
		Whether to overwrite document if it exists.
    quick:
        If True, skips collection schema checks
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "documents": documents,
            "insert_date": insert_date,
            "overwrite" : overwrite,
            "quick": quick
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/bulk_insert".format(self.url),
            json=params
        )
        return return_curl_or_response(response)
    
    @retry()
    def insert(self, collection_name: str, document: Dict, insert_date: bool=True, overwrite: bool=True,
    return_curl: bool=False, **kwargs):
        """
Insert a document into a Collection
When inserting the document you can specify your own id for a document by using the field name **"\_id"**. 
For specifying your own vector use the suffix (ends with)  **"\_vector\_"** for the field name.
e.g. "product\_description\_vector\_"
    
Args:
	collection_name:
		Name of Collection
	document:
		A Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
	insert_date:
		Whether to include insert date as a field 'insert_date_'.
	overwrite:
		Whether to overwrite document if it exists.
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document": document,
            "insert_date": insert_date,
            "overwrite" : overwrite
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/insert".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)
    
    @retry()
    def _edit_document(self, collection_name: str, edits: Dict, document_id: str, return_curl: bool=False, **kwargs):

        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "edits": edits,
            "document_id": document_id,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/edit_document".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def bulk_edit_document(self, collection_name: str, documents: List[Dict], return_curl: bool=False, **kwargs):
        """
        Edits documents by providing a key value pair of fields you are adding or changing, make sure to include the "_id" in the documents.
        Args:
            collection_name: Name of collection
            documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '_id', for specifying vector field use the suffix of '_vector_'
        """
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "documents": documents
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/bulk_edit_document".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def delete_by_id(self, collection_name: str, document_id: str, return_curl: bool=False, **kwargs):
        """
Delete a document in a Collection by its id
    
Args:
	document_id:
		ID of a document
	collection_name:
		Name of Collection
"""
        params={
            "username": self.username,
            "api_key": self.api_key,
            "collection_name": collection_name,
            "document_id": document_id,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/delete_by_id".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def publish_aggregation(
        self,
        collection_name: str,
        aggregation_query: dict,
        aggregation_name: str,
        aggregated_collection_name: str,
        description: str = "published aggregation",
        date_field: str = "insert_date_",
        refresh_time: int = 30,
        start_immediately: bool = True,
        return_curl: bool=False,
        **kwargs
    ):
        """
Publishes your aggregation query to a new collection
Publish and schedules your aggregation query and saves it to a new collection.
This new collection is just like any other collection and you can read, filter and aggregate it.
    
Args:
	source_collection:
		The collection where the data to aggregate comes from
	dest_collection:
		The name of collection of where the data will be aggregated to
	aggregation_name:
		The name for the published scheduled aggregation
	description:
		The description for the published scheduled aggregation
	aggregation_query:
		The aggregation query to schedule
	date_field:
		The date field to check whether there is new data coming in
	refresh_time:
		How often should the aggregation check for new data
	start_immediately:
		Whether to start the published aggregation immediately
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "aggregation_query": aggregation_query,
            "source_collection": collection_name,
            "dest_collection": aggregated_collection_name,
            "aggregation_name": aggregation_name,
            "description": description,
            "date_field": date_field,
            "refresh_time": "{}s".format(refresh_time),
            "start_immediately": start_immediately,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/publish_aggregation".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def start_aggregation(self, aggregation_name: str, return_curl: bool=False, **kwargs):
        """
Start your published aggregation
Start or resume your published aggregation. The published aggregation can be stopped with /stop_aggregation.
    
Args:
	aggregation_name:
		The name for the published scheduled aggregation
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "aggregation_name": aggregation_name,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/start_aggregation".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def stop_aggregation(self, aggregation_name: str, return_curl: bool=False, **kwargs):
        """
Stop your published aggregation
Stop/pause your published aggregation. The published aggregation can be resumed/started with /start_aggregation.
    
Args:
	aggregation_name:
		The name for the published scheduled aggregation
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "aggregation_name": aggregation_name,
        }
        params.update(kwargs)
        response = requests.get(
            url="{}/collection/stop_aggregation".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def delete_published_aggregation(self, aggregation_name: str, return_curl: bool=False):
        """
Delete a published aggregation and collection
Delete a published aggregation and the associated collection it creates.
    
Args:
	aggregation_name:
		The name for the published scheduled aggregation
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "aggregation_name": aggregation_name,
        }
        response = requests.get(
            url="{}/collection/delete_published_aggregation".format(self.url),
            params=params
        )
        return return_curl_or_response(response, 'json', return_curl)

    @retry()
    def join_collections(self, join_query: dict, joined_collection_name:str, return_curl: bool=False, **kwargs):
        """
Join collections with a query
Perform a join query on a whole collection and write the results to a new collection. We currently only support left joins.
    
Args:
	join_query:
		.
	joined_collection_name:
		Name of the new collection that contains the joined results
"""

        params={
            "username": self.username,
            "api_key": self.api_key,
            "join_query": join_query,
            "joined_collection_name": joined_collection_name,
        }
        params.update(kwargs)
        response = requests.post(
            url="{}/collection/join_collections".format(self.url),
            json=params
        )
        return return_curl_or_response(response, 'json', return_curl)
