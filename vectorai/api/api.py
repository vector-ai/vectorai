# This python file is auto-generated. Please do not edit.
import requests
import requests
from vectorai.api.utils import retry, return_curl_or_response


class _ViAPIClient:
	def __init__(self, username, api_key, url, ):
		self.username = username		
		self.api_key = api_key		
		self.url = url		

	@retry()
	@return_curl_or_response('json')
	def request_api_key(self, email, description, referral_code="api_referred", **kwargs):
		"""Request an api key
Make sure to save the api key somewhere safe. If you have a valid referral code, you can recieve the api key more quickly.
    
Args
========
username: Username you'd like to create, lowercase only
email: Email you are using to sign up
description: Description of your intended use case
referral_code: The referral code you've been given to allow you to register for an api key before others

"""
		return requests.post(
			url=self.url+'/project/request_api_key',
			json=dict(
				username=self.username,
				email=email, 
				description=description, 
				referral_code=referral_code, 
				))

	@retry()
	@return_curl_or_response('json')
	def list_jobs(self,show_active_only=True, **kwargs):
		return requests.get(
			url=self.url+'/project/list_jobs',
			params=dict(
				show_active_only=show_active_only, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def request_read_api_key(self, read_username, **kwargs):
		"""Request a read api key for your collections
Creates a read only key for your collections. Make sure to save the api key somewhere safe. When doing a search the admin username should still be used.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
read_username: Username for read only key

"""
		return requests.post(
			url=self.url+'/project/request_read_api_key',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				read_username=read_username, 
				))

	@retry()
	@return_curl_or_response('json')
	def _create_collection(self, collection_name, collection_schema={}, **kwargs):
		"""Creates a collection
A collection can store documents to be **searched, retrieved, filtered and aggregated** _(similar to Collections in MongoDB, Tables in SQL, Indexes in ElasticSearch)_.

If you are inserting your own vector use the suffix (ends with) **"\_vector\_"** for the field name. and specify the length of the vector in colletion_schema like below example:

    {
        "collection_schema": {
            "celebrity_image_vector_": 1024,
            "celebrity_audio_vector" : 512,
            "product_description_vector" : 128
        }
    }
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
collection_schema: Schema for specifying the field that are vectors and its length

"""
		return requests.post(
			url=self.url+'/project/create_collection',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				collection_schema=collection_schema, 
				))

	@retry()
	@return_curl_or_response('json')
	def _create_collection_from_document(self, collection_name, document={}, **kwargs):
		"""Creates a collection by infering the schema from a document
If you are inserting your own vector use the suffix (ends with)  **"\_vector\_"** for the field name. e.g. "product\_description\_vector\_"
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document: A Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'

"""
		return requests.post(
			url=self.url+'/project/create_collection_from_document',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				))

	@retry()
	@return_curl_or_response('json')
	def _delete_collection(self,collection_name, **kwargs):
		return requests.get(
			url=self.url+'/project/delete_collection',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def _list_collections(self,sort_by_created_at_date=False, asc=False, **kwargs):
		return requests.get(
			url=self.url+'/project/list_collections',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				sort_by_created_at_date=sort_by_created_at_date, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_collections(self, collection_search_query, sort_by_created_at_date=False, asc=False, **kwargs):
		"""Search collections
Search collections by their names
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_search_query: The collection search query
sort_by_created_at_date: Sort by created at date. By default shows the newest collections. Set reverse=False to get oldest collection.
asc: Sort by created at date. By default shows the newest collections. Set reverse=False to get oldest collection.

"""
		return requests.post(
			url=self.url+'/project/search_collections',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_search_query=collection_search_query, 
				sort_by_created_at_date=sort_by_created_at_date, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def list_collections_info(self,schema=True, stats=True, metadata=True, schema_stats=False, vector_health=False, active_jobs=False, collection_names=[], sort_by_created_at_date=False, asc=False, page_size=20, page=1, **kwargs):
		return requests.get(
			url=self.url+'/project/list_collections_info',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				schema=schema, 
				stats=stats, 
				metadata=metadata, 
				schema_stats=schema_stats, 
				vector_health=vector_health, 
				active_jobs=active_jobs, 
				collection_names=collection_names, 
				sort_by_created_at_date=sort_by_created_at_date, 
				asc=asc, 
				page_size=page_size, 
				page=page, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_stats(self,collection_name, seperate_chunks=False, **kwargs):
		return requests.get(
			url=self.url+'/project/collection_stats',
			params=dict(
				seperate_chunks=seperate_chunks, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_schema(self,collection_name, **kwargs):
		return requests.get(
			url=self.url+'/project/collection_schema',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_schema_stats(self,collection_name, include_zero_vectors=True, **kwargs):
		return requests.get(
			url=self.url+'/project/collection_schema_stats',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				include_zero_vectors=include_zero_vectors, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_vector_health(self,collection_name, **kwargs):
		return requests.get(
			url=self.url+'/project/collection_vector_health',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def add_collection_metadata(self, collection_name, metadata, **kwargs):
		"""Add metadata about a collection
Add metadata about a collection. notably description, data source, etc
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
metadata: Metadata for a collection, e.g. {'description' : 'collection for searching products'}

"""
		return requests.post(
			url=self.url+'/project/add_collection_metadata',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				metadata=metadata, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_metadata(self,collection_name, **kwargs):
		return requests.get(
			url=self.url+'/project/collection_metadata',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def copy_collection(self, collection_name, original_collection_name, collection_schema={}, rename_fields={}, remove_fields=[], **kwargs):
		"""Copy a collection into a new collection
Copy a collection into a new collection. You can use this to rename fields and change data schema. This is considered a project job.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
original_collection_name: Name of collection to copy from
collection_schema: Schema to change, if unspecified then schema is unchanged. Defaults to no schema change
rename_fields: Fields to rename {'old_field': 'new_field'}. Defaults to no renames
remove_fields: Fields to remove ['random_field', 'another_random_field']. Defaults to no removes

"""
		return requests.post(
			url=self.url+'/project/copy_collection',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				original_collection_name=original_collection_name, 
				collection_schema=collection_schema, 
				rename_fields=rename_fields, 
				remove_fields=remove_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def job_status(self,job_id, **kwargs):
		return requests.get(
			url=self.url+'/project/job/job_status',
			params=dict(
				job_id=job_id, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def insert(self, collection_name, document={}, insert_date=True, overwrite=True, update_schema=True, quick=False, pipeline=[], **kwargs):
		"""Insert a document into a Collection
When inserting the document you can specify your own id for a document by using the field name **"\_id"**. 
For specifying your own vector use the suffix (ends with)  **"\_vector\_"** for the field name.
e.g. "product\_description\_vector\_"
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document: A Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.
overwrite: Whether to overwrite document if it exists.
update_schema: Whether the api should check the documents for vector datatype to update the schema.
quick: This will run the quickest insertion possible, which means there will be no schema checks or collection checks.
pipeline: This will run pipelines for the insert. example: pipeline=["encoders"]

"""
		return requests.post(
			url=self.url+'/collection/insert',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				update_schema=update_schema, 
				quick=quick, 
				pipeline=pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def insert_and_encode(self, encoders, collection_name, document={}, insert_date=True, overwrite=True, update_schema=True, quick=False, store_to_pipeline=True, **kwargs):
		"""Insert and encode document into a Collection
Insert a document and encode specified fields into vectors with provided model urls or model names. 

    {
        "thumbnail" : {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url"},
        "short_description" : {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text"},
        "short_description" : {"model_url" : "bert", "alias" : "bert"},
    }

This primarily uses deployed models.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
encoders: An array structure of models to encode fields with.
    Encoders can be a `model_url` or a `model_name`.
    For model_name, the options are: `image_text`, `image`, `text`. `text_multi`, `text_image`.
    Note: image_text encodes images for text to image search whereas text_image encodes texts
    for text to image search (text to image search/image to text search works both ways).
    For model_url, you are free to deploy your own model and specify the required body as such.

    [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_name" : "text", "body" : "text", "field": "short_description", "alias":"bert"},
        {"model_name" : "image_text", "body" : "url", "field" : "thumbnail"},
    ]
    
collection_name: Name of Collection
document: A Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.
overwrite: Whether to overwrite document if it exists.
update_schema: Whether the api should check the documents for vector datatype to update the schema.
quick: This will run the quickest insertion possible, which means there will be no schema checks or collection checks.
store_to_pipeline: Whether to store the encoders to pipeline

"""
		return requests.post(
			url=self.url+'/collection/insert_and_encode',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				encoders=encoders, 
				collection_name=collection_name, 
				document=document, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				update_schema=update_schema, 
				quick=quick, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_insert(self, collection_name, documents={}, insert_date=True, overwrite=True, update_schema=True, quick=False, pipeline=[], **kwargs):
		"""Insert multiple documents into a Collection
When inserting the document you can specify your own id for a document by using the field name **"\_id"**. 
For specifying your own vector use the suffix (ends with)  **"\_vector\_"** for the field name.
e.g. "product\_description\_vector\_"
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.
overwrite: Whether to overwrite document if it exists.
update_schema: Whether the api should check the documents for vector datatype to update the schema.
quick: This will run the quickest insertion possible, which means there will be no schema checks or collection checks.
pipeline: This will run pipelines for the insert. example: pipeline=["encoders"]

"""
		return requests.post(
			url=self.url+'/collection/bulk_insert',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				documents=documents, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				update_schema=update_schema, 
				quick=quick, 
				pipeline=pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_insert_and_encode(self, encoders, collection_name, documents={}, insert_date=True, overwrite=True, update_schema=True, quick=False, store_to_pipeline=True, **kwargs):
		"""Insert and encode multiple documents into a Collection
Insert multiple document and encode specified fields into vectors with provided model urls or model names. [
        {"model_url" : ""https://a_vector_model_url.com/encode_image_url"", "body" : "url", "field" : "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field" : "short_description"},
        {"model_url" : "text", "alias" : "bert", "field" : "short_description"},
    ]
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
encoders: An array structure of models to encode fields with.
    Encoders can be a `model_url` or a `model_name`.
    For model_name, the options are: `image_text`, `image`, `text`. `text_multi`, `text_image`.
    Note: image_text encodes images for text to image search whereas text_image encodes texts
    for text to image search (text to image search/image to text search works both ways).
    For model_url, you are free to deploy your own model and specify the required body as such.

    [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_name" : "text", "body" : "text", "field": "short_description", "alias":"bert"},
        {"model_name" : "image_text", "body" : "url", "field" : "thumbnail"},
    ]
    
collection_name: Name of Collection
documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.
overwrite: Whether to overwrite document if it exists.
update_schema: Whether the api should check the documents for vector datatype to update the schema.
quick: This will run the quickest insertion possible, which means there will be no schema checks or collection checks.
store_to_pipeline: Whether to store the encoders to pipeline

"""
		return requests.post(
			url=self.url+'/collection/bulk_insert_and_encode',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				encoders=encoders, 
				collection_name=collection_name, 
				documents=documents, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				update_schema=update_schema, 
				quick=quick, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def store_encoders_pipeline(self, encoders, collection_name, **kwargs):
		"""Store encoder to the collection's pipeline
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
encoders: An array structure of models to encode fields with.
    Encoders can be a `model_url` or a `model_name`.
    For model_name, the options are: `image_text`, `image`, `text`. `text_multi`, `text_image`.
    Note: image_text encodes images for text to image search whereas text_image encodes texts
    for text to image search (text to image search/image to text search works both ways).
    For model_url, you are free to deploy your own model and specify the required body as such.

    [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_name" : "text", "body" : "text", "field": "short_description", "alias":"bert"},
        {"model_name" : "image_text", "body" : "url", "field" : "thumbnail"},
    ]
    
collection_name: Name of Collection

"""
		return requests.post(
			url=self.url+'/collection/store_encoders_pipeline',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				encoders=encoders, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def remove_encoder_from_pipeline(self, collection_name, vector_fields, **kwargs):
		"""Remove an encoder from the collection's encoders pipeline
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vector_fields: Vector fields that identifies an encoder to remove from pipeline

"""
		return requests.post(
			url=self.url+'/collection/remove_encoder_from_pipeline',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector_fields=vector_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def delete_by_id(self,document_id, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/delete_by_id',
			params=dict(
				document_id=document_id, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_delete_by_id(self, collection_name, document_ids, **kwargs):
		"""Delete multiple documents in a Collection by ids
Delete multiple document by its ids.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document_ids: IDs of documents

"""
		return requests.post(
			url=self.url+'/collection/bulk_delete_by_id',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document_ids=document_ids, 
				))

	@retry()
	@return_curl_or_response('json')
	def edit_document(self, collection_name, document_id, edits, insert_date=True, **kwargs):
		"""Edit a document in a Collection by its id
Edit by providing a key value pair of fields you are adding or changing.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document_id: ID of a document
edits: A dictionary to edit and add fields to a document.
insert_date: Whether to include insert date as a field 'insert_date_'.

"""
		return requests.post(
			url=self.url+'/collection/edit_document',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document_id=document_id, 
				edits=edits, 
				insert_date=insert_date, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_edit_document(self, collection_name, documents={}, insert_date=True, **kwargs):
		"""Edits multiple documents in a Collection by its ids
Edits documents by providing a key value pair of fields you are adding or changing, make sure to include the "_id" in the documents.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.

"""
		return requests.post(
			url=self.url+'/collection/bulk_edit_document',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				documents=documents, 
				insert_date=insert_date, 
				))

	@retry()
	@return_curl_or_response('json')
	def delete_document_fields(self,document_id, fields_to_delete, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/delete_document_fields',
			params=dict(
				document_id=document_id, 
				fields_to_delete=fields_to_delete, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def update_by_filters(self, collection_name, updates, filters=[], **kwargs):
		"""Updates documents by filters
Updates documents by filters. The updates to make to the documents that is returned by a filter. The updates should be specified in a format of {"field_name": "value"}. e.g. {"item.status" : "Sold Out"}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
updates: Updates to make to the documents. It should be specified in a format of {"field_name": "value"}. e.g. {"item.status" : "Sold Out"}
filters: Query for filtering the search results

"""
		return requests.post(
			url=self.url+'/collection/update_by_filters',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				updates=updates, 
				filters=filters, 
				))

	@retry()
	@return_curl_or_response('json')
	def delete_by_filters(self, collection_name, filters=[], **kwargs):
		"""Delete documents by filters
Delete documents by filters.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
filters: Query for filtering the search results

"""
		return requests.post(
			url=self.url+'/collection/delete_by_filters',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				filters=filters, 
				))

	@retry()
	@return_curl_or_response('json')
	def edit_search_history(self, collection_name, search_history_id, edits, **kwargs):
		"""Edit search history by its id
Edit search history by providing a key value pair of fields you are adding or changing.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
search_history_id: Search history ID of the collection.
edits: A dictionary to edit and add fields to a document.

"""
		return requests.post(
			url=self.url+'/collection/edit_search_history',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				search_history_id=search_history_id, 
				edits=edits, 
				))

	@retry()
	@return_curl_or_response('json')
	def id(self,document_id, collection_name, include_vector=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/id',
			params=dict(
				document_id=document_id, 
				include_vector=include_vector, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_id(self,document_ids, collection_name, include_vector=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/bulk_id',
			params=dict(
				document_ids=document_ids, 
				include_vector=include_vector, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_missing_id(self, collection_name, document_ids, **kwargs):
		"""Look up in bulk if the ids exists in the collection, returns all the missing one as a list
Look up in bulk if the ids exists in the collection, returns all the missing one as a list.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document_ids: IDs of documents

"""
		return requests.post(
			url=self.url+'/collection/bulk_missing_id',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document_ids=document_ids, 
				))

	@retry()
	@return_curl_or_response('json')
	def retrieve_documents(self,collection_name, include_fields=[], cursor=None, page_size=20, sort=[], asc=False, include_vector=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/retrieve_documents',
			params=dict(
				include_fields=include_fields, 
				cursor=cursor, 
				page_size=page_size, 
				sort=sort, 
				asc=asc, 
				include_vector=include_vector, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def random_documents(self,collection_name, seed=10, include_fields=[], page_size=20, include_vector=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/random_documents',
			params=dict(
				seed=seed, 
				include_fields=include_fields, 
				page_size=page_size, 
				include_vector=include_vector, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def retrieve_documents_with_filters(self, collection_name, include_fields=[], cursor=None, page_size=20, sort=[], asc=False, include_vector=True, filters=[], **kwargs):
		"""Retrieve some documents with filters
Retrieve documents with filters.
Cursor is provided to retrieve even more documents. Loop through it to retrieve all documents in the database.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
include_fields: Fields to include in the search results, empty array/list means all fields.
cursor: Cursor to paginate the document retrieval
page_size: Size of each page of results
sort: Fields to sort by
asc: Whether to sort results by ascending or descending order
include_vector: Include vectors in the search results
filters: Query for filtering the search results

"""
		return requests.post(
			url=self.url+'/collection/retrieve_documents_with_filters',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				include_fields=include_fields, 
				cursor=cursor, 
				page_size=page_size, 
				sort=sort, 
				asc=asc, 
				include_vector=include_vector, 
				filters=filters, 
				))

	@retry()
	@return_curl_or_response('json')
	def random_documents_with_filters(self, collection_name, seed=10, include_fields=[], page_size=20, include_vector=True, filters=[], **kwargs):
		"""Retrieve some documents randomly with filters
Mainly for testing purposes.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
seed: Random Seed for retrieving random documents.
include_fields: Fields to include in the search results, empty array/list means all fields.
page_size: Size of each page of results
include_vector: Include vectors in the search results
filters: Query for filtering the search results

"""
		return requests.post(
			url=self.url+'/collection/random_documents_with_filters',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				seed=seed, 
				include_fields=include_fields, 
				page_size=page_size, 
				include_vector=include_vector, 
				filters=filters, 
				))

	@retry()
	@return_curl_or_response('json')
	def compare_documents(self, doc, docs_to_compare, difference_fields=[], **kwargs):
		"""Compare the differences between a document against multiple other documents
Compare the differences between a document and multiple other documents.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
doc: Main document to compare other documents against.
docs_to_compare: Other documents to compare against the main document.
difference_fields: Fields to compare. Defaults to [], which compares all fields.

"""
		return requests.post(
			url=self.url+'/collection/compare_documents',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				doc=doc, 
				docs_to_compare=docs_to_compare, 
				difference_fields=difference_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def retrieve_search_history(self,**kwargs):
		return requests.get(
			url=self.url+'/collection/retrieve_search_history',
			params=dict(
				))

	@retry()
	@return_curl_or_response('json')
	def id_search_history(self,**kwargs):
		return requests.get(
			url=self.url+'/collection/id_search_history',
			params=dict(
				))

	@retry()
	@return_curl_or_response('json')
	def _search(self,vector, collection_name, search_fields, search_history_id, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, keep_search_history=True, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, **kwargs):
		return requests.get(
			url=self.url+'/collection/search',
			params=dict(
				vector=vector, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_fields=search_fields, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				search_history_id=search_history_id, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_by_id(self,document_id, collection_name, search_field, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, **kwargs):
		return requests.get(
			url=self.url+'/collection/search_by_id',
			params=dict(
				document_id=document_id, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_field=search_field, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_by_ids(self,document_ids, collection_name, search_field, vector_operation="sum", approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, **kwargs):
		return requests.get(
			url=self.url+'/collection/search_by_ids',
			params=dict(
				document_ids=document_ids, 
				vector_operation=vector_operation, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_field=search_field, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_by_positive_negative_ids(self,positive_document_ids, negative_document_ids, collection_name, search_field, vector_operation="sum", approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, **kwargs):
		return requests.get(
			url=self.url+'/collection/search_by_positive_negative_ids',
			params=dict(
				positive_document_ids=positive_document_ids, 
				negative_document_ids=negative_document_ids, 
				vector_operation=vector_operation, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_field=search_field, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_positive_negative_ids_as_history(self,vector, positive_document_ids, negative_document_ids, collection_name, search_field, vector_operation="sum", approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, **kwargs):
		return requests.get(
			url=self.url+'/collection/search_with_positive_negative_ids_as_history',
			params=dict(
				vector=vector, 
				positive_document_ids=positive_document_ids, 
				negative_document_ids=negative_document_ids, 
				vector_operation=vector_operation, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_field=search_field, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode(self, encoders, document, **kwargs):
		"""Encode document into vectors
Get a document and encode specified fields into vectors with provided model urls or model names. [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_url" : "bert", "body" : "text", "field": "short_description", "alias":"bert"},
    ]
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
encoders: An array structure of models to encode fields with.
    Encoders can be a `model_url` or a `model_name`.
    For model_name, the options are: `image_text`, `image`, `text`. `text_multi`, `text_image`.
    Note: image_text encodes images for text to image search whereas text_image encodes texts
    for text to image search (text to image search/image to text search works both ways).
    For model_url, you are free to deploy your own model and specify the required body as such.

    [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_name" : "text", "body" : "text", "field": "short_description", "alias":"bert"},
        {"model_name" : "image_text", "body" : "url", "field" : "thumbnail"},
    ]
    
document: A json document to encode.

"""
		return requests.post(
			url=self.url+'/collection/encode',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				encoders=encoders, 
				document=document, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_encode(self, encoders, documents, **kwargs):
		"""Bulk encode document into vectors
Get a document and encode specified fields into vectors with provided model urls or model names. {
    [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_url" : "bert", "body" : "text", "field": "short_description", "alias":"bert"},
    ]
    }
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
encoders: An array structure of models to encode fields with.
    Encoders can be a `model_url` or a `model_name`.
    For model_name, the options are: `image_text`, `image`, `text`. `text_multi`, `text_image`.
    Note: image_text encodes images for text to image search whereas text_image encodes texts
    for text to image search (text to image search/image to text search works both ways).
    For model_url, you are free to deploy your own model and specify the required body as such.

    [
        {"model_url" : "https://a_vector_model_url.com/encode_image_url", "body" : "url", "field": "thumbnail"},
        {"model_url" : "https://a_vector_model_url.com/encode_text", "body" : "text", "field": "short_description"},
        {"model_name" : "text", "body" : "text", "field": "short_description", "alias":"bert"},
        {"model_name" : "image_text", "body" : "url", "field" : "thumbnail"},
    ]
    
documents: Json documents to encode.

"""
		return requests.post(
			url=self.url+'/collection/bulk_encode',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				encoders=encoders, 
				documents=documents, 
				))

	@retry()
	@return_curl_or_response('json')
	def predict_knn_regression(self, collection_name, vector, search_field, target_field, impute_value, k=5, weighting=True, predict_operation="mean", **kwargs):
		"""Predict KNN regression.
Predict with KNN regression using normal search.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vector: Vector, a list/array of floats that represents a piece of data
search_field: The field to search with.
target_field: The field to perform regression on.
k: The number of results for KNN.
weighting: weighting
impute_value: What value to fill if target field is missing.
predict_operation: How to predict using the vectors.

"""
		return requests.post(
			url=self.url+'/collection/predict_knn_regression',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector=vector, 
				search_field=search_field, 
				target_field=target_field, 
				k=k, 
				weighting=weighting, 
				impute_value=impute_value, 
				predict_operation=predict_operation, 
				))

	@retry()
	@return_curl_or_response('json')
	def predict_knn_regression_from_results(self, field, results, impute_value, weighting=True, predict_operation="mean", **kwargs):
		"""Predict KNN regression from search results
Predict using KNN regression from search results
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
field: Field in results to weigh on.
results: List of results in a dictionary
weighting: weighting of the actual vectors
impute_value: The impute value
predict_operation: How to predict using the vectors.

"""
		return requests.post(
			url=self.url+'/collection/predict_knn_regression_from_results',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				field=field, 
				results=results, 
				weighting=weighting, 
				impute_value=impute_value, 
				predict_operation=predict_operation, 
				))

	@retry()
	@return_curl_or_response('json')
	def facets(self,collection_name, facets_fields=[], date_interval="monthly", page_size=1000, page=1, asc=False, **kwargs):
		return requests.get(
			url=self.url+'/collection/facets',
			params=dict(
				facets_fields=facets_fields, 
				date_interval=date_interval, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def filters(self, collection_name, filters=[], page=1, page_size=20, asc=False, include_vector=False, sort=[], **kwargs):
		"""Filters a collection
Filter is used to retrieve documents that match the conditions set in a filter query. This is used in advance search to filter the documents that are searched.

The filters query is a json body that follows the schema of:

    [
        {'field' : <field to filter>, 'filter_type' : <type of filter>, "condition":"==", "condition_value":"america"},
        {'field' : <field to filter>, 'filter_type' : <type of filter>, "condition":">=", "condition_value":90},
    ]

These are the available filter_type types:

1. "contains": for filtering documents that contains a string.
        {'field' : 'item_brand', 'filter_type' : 'contains', "condition":"==", "condition_value": "samsu"}
2. "exact_match"/"category": for filtering documents that matches a string or list of strings exactly.
        {'field' : 'item_brand', 'filter_type' : 'category', "condition":"==", "condition_value": "sumsung"}
3. "categories": for filtering documents that contains any of a category from a list of categories.
        {'field' : 'item_category_tags', 'filter_type' : 'categories', "condition":"==", "condition_value": ["tv", "smart", "bluetooth_compatible"]}
4. "exists": for filtering documents that contains a field.
        {'field' : 'purchased', 'filter_type' : 'exists', "condition":"==", "condition_value":" "}
If you are looking to filter for documents where a field doesn't exist, run this:
        {'field' : 'purchased', 'filter_type' : 'exists', "condition":"!=", "condition_value":" "}
5. "date": for filtering date by date range.
        {'field' : 'insert_date_', 'filter_type' : 'date', "condition":">=", "condition_value":"2020-01-01"}
6. "numeric": for filtering by numeric range.
        {'field' : 'price', 'filter_type' : 'numeric', "condition":">=", "condition_value":90}
7. "ids": for filtering by document ids.
        {'field' : 'ids', 'filter_type' : 'ids', "condition":"==", "condition_value":["1", "10"]}

These are the available conditions:

    "==", "!=", ">=", ">", "<", "<="
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
filters: Query for filtering the search results
page: Page of the results
page_size: Size of each page of results
asc: Whether to sort results by ascending or descending order
include_vector: Include vectors in the search results
sort: Fields to sort by

"""
		return requests.post(
			url=self.url+'/collection/filters',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				filters=filters, 
				page=page, 
				page_size=page_size, 
				asc=asc, 
				include_vector=include_vector, 
				sort=sort, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_search(self, collection_name, multivector_query, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Vector Similarity Search. Support for multiple vectors, vector weightings, facets and filtering
Advanced Vector Similarity Search, enables machine learning search with vector search. Search with a multiple vectors for the most similar documents.

For example: Search with a product image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
multivector_query: Query for advance search that allows for multiple vector and field querying

"""
		return requests.post(
			url=self.url+'/collection/advanced_search',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				multivector_query=multivector_query, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_by_id(self, collection_name, document_id, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Single Product Recommendations
Single Product Recommendations (Search by an id).

For example: Search with id of a product in the database, and using the product's image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
document_id: ID of a document
search_fields: Vector fields to search against, and the weightings for them.

"""
		return requests.post(
			url=self.url+'/collection/advanced_search_by_id',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				document_id=document_id, 
				search_fields=search_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_by_ids(self, collection_name, document_ids, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, vector_operation="sum", **kwargs):
		"""Advanced Multi Product Recommendations
Advanced Multi Product Recommendations (Search by ids).

For example: Search with multiple ids of products in the database, and using the product's image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

You can also give weightings of on each product as well e.g. product ID-A weights 100% whilst product ID-B 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
document_ids: Document IDs to get recommendations for, and the weightings of each document
search_fields: Vector fields to search against, and the weightings for them.
vector_operation: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']

"""
		return requests.post(
			url=self.url+'/collection/advanced_search_by_ids',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				document_ids=document_ids, 
				search_fields=search_fields, 
				vector_operation=vector_operation, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_by_positive_negative_ids(self, collection_name, positive_document_ids, negative_document_ids, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, vector_operation="sum", **kwargs):
		"""Advanced Multi Product Recommendations with likes and dislikes
Advanced Multi Product Recommendations with Likes and Dislikes (Search by ids).

For example: Search with multiple ids of liked and dislike products in the database. Then using the product's image and description vectors to find the most similar products by what it looks like and what its described to do against the positives and most disimilar products for the negatives.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

You can also give weightings of on each product as well e.g. product ID-A weights 100% whilst product ID-B 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
positive_document_ids: Positive Document IDs to get recommendations for, and the weightings of each document
negative_document_ids: Negative Document IDs to get recommendations for, and the weightings of each document
search_fields: Vector fields to search against, and the weightings for them.
vector_operation: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']

"""
		return requests.post(
			url=self.url+'/collection/advanced_search_by_positive_negative_ids',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				positive_document_ids=positive_document_ids, 
				negative_document_ids=negative_document_ids, 
				search_fields=search_fields, 
				vector_operation=vector_operation, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_with_positive_negative_ids_as_history(self, collection_name, multivector_query, positive_document_ids, negative_document_ids, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, vector_operation="sum", **kwargs):
		"""Advanced Search with Likes and Dislikes as history
For example: Vector search of a query vector with multiple ids of liked and dislike products in the database. Then using the product's image and description vectors to find the most similar products by what it looks like and what its described to do against the positives and most disimilar products for the negatives.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

You can also give weightings of on each product as well e.g. product ID-A weights 100% whilst product ID-B 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
multivector_query: Query for advance search that allows for multiple vector and field querying
positive_document_ids: Positive Document IDs to get recommendations for, and the weightings of each document
negative_document_ids: Negative Document IDs to get recommendations for, and the weightings of each document
vector_operation: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']

"""
		return requests.post(
			url=self.url+'/collection/advanced_search_with_positive_negative_ids_as_history',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				multivector_query=multivector_query, 
				positive_document_ids=positive_document_ids, 
				negative_document_ids=negative_document_ids, 
				vector_operation=vector_operation, 
				))

	@retry()
	@return_curl_or_response('json')
	def aggregate(self, collection_name, aggregation_query, filters=[], page_size=20, page=1, asc=False, flatten=True, **kwargs):
		"""Aggregate a collection
Aggregation/Groupby of a collection using an aggregation query.
The aggregation query is a json body that follows the schema of:

    {
        "groupby" : [
            {"name": <alias>, "field": <field in the collection>, "agg": "category"},
            {"name": <alias>, "field": <another groupby field in the collection>, "agg": "numeric"}
        ],
        "metrics" : [
            {"name": <alias>, "field": <numeric field in the collection>, "agg": "avg"}
            {"name": <alias>, "field": <another numeric field in the collection>, "agg": "max"}
        ]
    }
    For example, one can use the following aggregations to group score based on region and player name.
    {
        "groupby" : [
            {"name": "region", "field": "player_region", "agg": "category"},
            {"name": "player_name", "field": "name", "agg": "category"}
        ],
        "metrics" : [
            {"name": "average_score", "field": "final_score", "agg": "avg"},
            {"name": "max_score", "field": "final_score", "agg": "max"},
            {'name':'total_score','field':"final_score", 'agg':'sum'},
            {'name':'average_deaths','field':"final_deaths", 'agg':'avg'},
            {'name':'highest_deaths','field':"final_deaths", 'agg':'max'},
        ]
    }
- "groupby" is the fields you want to split the data into. These are the available groupby types:
    - category" : groupby a field that is a category
    - numeric: groupby a field that is a numeric
- "metrics" is the fields you want to metrics you want to calculate in each of those, every aggregation includes a frequency metric. These are the available metric types:
    - "avg", "max", "min", "sum", "cardinality"
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
filters: Query for filtering the search results
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 

"""
		return requests.post(
			url=self.url+'/collection/aggregate',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				filters=filters, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				))

	@retry()
	@return_curl_or_response('json')
	def aggregate_fetch(self, collection_name, aggregation_query, filters=[], page_size=20, page=1, asc=False, flatten=True, **kwargs):
		"""Aggregate a collection and fetch the documents
Perform an aggregation and then a Bulk ID Lookup using IDs of the aggregated results to get the documents alongside the aggregations.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
filters: Query for filtering the search results
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 

"""
		return requests.post(
			url=self.url+'/collection/aggregate_fetch',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				filters=filters, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				))

	@retry()
	@return_curl_or_response('json')
	def traditional_search(self,collection_name, text, text_fields, search_history_id, fuzzy=-1, join=True, page_size=20, page=1, include_fields=[], include_vector=False, include_count=True, asc=False, keep_search_history=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/traditional_search',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				text=text, 
				text_fields=text_fields, 
				fuzzy=fuzzy, 
				join=join, 
				page_size=page_size, 
				page=page, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				search_history_id=search_history_id, 
				))

	@retry()
	@return_curl_or_response('json')
	def hybrid_search(self,text, vector, text_fields, collection_name, search_fields, search_history_id, traditional_weight=0.075, fuzzy=-1, join=True, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, keep_search_history=True, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, **kwargs):
		return requests.get(
			url=self.url+'/collection/hybrid_search',
			params=dict(
				text=text, 
				vector=vector, 
				text_fields=text_fields, 
				traditional_weight=traditional_weight, 
				fuzzy=fuzzy, 
				join=join, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_fields=search_fields, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				search_history_id=search_history_id, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_hybrid_search(self, collection_name, multivector_query, text, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, text_fields=[], traditional_weight=0.075, fuzzy=-1, join=True, **kwargs):
		"""Advanced Search a text field with vector and text using Vector Search and Traditional Search
Advanced Vector similarity search + Traditional Fuzzy Search with text and vector.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
multivector_query: Query for advance search that allows for multiple vector and field querying
text: Text Search Query (not encoded as vector)
text_fields: Text fields to search against
traditional_weight: Multiplier of traditional search. A value of 0.025~0.1 is good.
fuzzy: Fuzziness of the search. A value of 1-3 is good. For automated fuzzines use -1.
join: Whether to consider cases where there is a space in the word. E.g. Go Pro vs GoPro.

"""
		return requests.post(
			url=self.url+'/collection/advanced_hybrid_search',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				multivector_query=multivector_query, 
				text=text, 
				text_fields=text_fields, 
				traditional_weight=traditional_weight, 
				fuzzy=fuzzy, 
				join=join, 
				))

	@retry()
	@return_curl_or_response('json')
	def job_status(self,job_id, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/job/job_status',
			params=dict(
				job_id=job_id, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def list_collection_jobs(self,collection_name, show_active_only=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/job/list_collection_jobs',
			params=dict(
				show_active_only=show_active_only, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_image_field(self, collection_name, image_field, task="image", alias="", refresh=False, store_to_pipeline=True, **kwargs):
		"""Start job to encode image field
Encode an image field with a model to add vectors to the collection, you can specify the task of "image" or "image_text".
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
image_field: The document image field to encode.
task: The name of the task for the job. "image" for encoding image fields with image based models, "image_text" for encoding images that can be searched against text
alias: Alias is used to uniquely identify vector fields
refresh: If True, overwrite all encoded vectors, otherwise it just encodes the fields that don't have vectors.
store_to_pipeline: Whether to store the encoder to the encoders pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/encode_image_field',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				image_field=image_field, 
				task=task, 
				alias=alias, 
				refresh=refresh, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_text_field(self, collection_name, text_field, task="text", alias="", refresh=False, store_to_pipeline=True, **kwargs):
		"""Start job to encode text field
Encode a text field with a model to add vectors to the collection, you can specify the task of "text", "text_image" or "text_multi".
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
text_field: The document text field to encode.
task: The name of the task for the job. "text" for encoding english models, "text_multi" for encoding multilanguage models, "text_image" for encoding text that can be searched with images
alias: Alias is used to uniquely identify vector fields
refresh: If True, overwrite all encoded vectors, otherwise it just encodes the fields that don't have vectors.
store_to_pipeline: Whether to store the encoder to the encoders pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/encode_text_field',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				text_field=text_field, 
				task=task, 
				alias=alias, 
				refresh=refresh, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster(self, collection_name, vector_field, n_clusters, alias="default", task="cluster", n_iter=10, n_init=5, refresh=False, store_to_pipeline=True, **kwargs):
		"""Start job to cluster a vector field
Clusters a collection into groups using unsupervised machine learning. Clusters can then be aggregated to understand whats in them and how vectors are seperating data into different groups.
Advanced cluster allows for more parameters to tune and alias to name each differently trained clusters.
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vector_field: Vector field to perform clustering on
alias: Alias is used to name a cluster
task: The name of the task for the job.
n_clusters: Number of clusters
n_iter: Number of iterations in each run
n_init: Number of runs to run with different centroid seeds
refresh: If True, overwrite all labelled clusters, otherwise it just labels the fields that don't have clusters.
store_to_pipeline: Whether to store the cluster model to the clusters pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/advanced_cluster',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector_field=vector_field, 
				alias=alias, 
				task=task, 
				n_clusters=n_clusters, 
				n_iter=n_iter, 
				n_init=n_init, 
				refresh=refresh, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def dimensionality_reduction(self, collection_name, vector_field, n_components, alias="default", task="dimensionality_reduction", refresh=False, store_to_pipeline=True, **kwargs):
		"""Start job to dimensionality reduce a vector field
Dimensionality reduction allows your vectors to be reduced down to any dimensions greater than 0 using unsupervised machine learning. 

This is useful for even faster search and visualising the vectors.
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vector_field: Vector field to perform dimensionality reduction on
alias: Alias is used to name a dimensionality reduced vector field
task: The name of the task for the job.
n_components: The size/length to reduce the vector down to. If 0 is set then highest possible is of components is set, when this is done you can get reduction on demand of any length.
refresh: If True, overwrite all labelled dimensionality reduced fields, otherwise it just adds the fields that don't have dimensionality reduced fields.
store_to_pipeline: Whether to store the dimensionality reduction model to the dimensionality reductions pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/dimensionality_reduction',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector_field=vector_field, 
				alias=alias, 
				task=task, 
				n_components=n_components, 
				refresh=refresh, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def tag_vector_job(self, collection_name, tag_collection_name, vector_field, hub_username, hub_api_key, tag_field="tag", tag_vector_field="tag_vector_", field="", alias="default", metric="cosine", number_of_tags=5, include_tag_vector=True, refresh=False, store_to_pipeline=True, **kwargs):
		"""Start job for tagging vectors
Search for a tag and then encode
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
tag_collection_name: Name of the collection you are retrieving the tags from
vector_field: vector field from the source collection to tag on
tag_field: The field in the tag collection to use for tagging.
tag_vector_field: vector field in the tag collection, used for matching the vectors to tag.
field: The field in the source collection to be tagged.
alias: The alias of the tags. Defaults to 'default'
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
number_of_tags: The number of tags to retrieve.
include_tag_vector: Whether to include the one hot encoded tag vector.
refresh: If True, Re-tags from scratch.
hub_username: The username of the hub account.
hub_api_key: The API key of the hub account.
store_to_pipeline: Whether to store the encoders to pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/tag_vector_job',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				tag_collection_name=tag_collection_name, 
				vector_field=vector_field, 
				tag_field=tag_field, 
				tag_vector_field=tag_vector_field, 
				field=field, 
				alias=alias, 
				metric=metric, 
				number_of_tags=number_of_tags, 
				include_tag_vector=include_tag_vector, 
				refresh=refresh, 
				hub_username=hub_username, 
				hub_api_key=hub_api_key, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def tag_job(self, collection_name, tag_collection_name, hub_username, hub_api_key, field="", encoder_task="text", tag_field="tag", tag_vector_field="tag_vector_", alias="default", metric="cosine", number_of_tags=5, include_tag_vector=True, refresh=False, store_to_pipeline=True, **kwargs):
		"""Start a job for encoding a field and then tagging
Encode using an encoder and tag
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
tag_collection_name: Name of the collection you are retrieving the tags from
field: The field in the source collection to be tagged.
encoder_task: Name of the task to run an encoding job on. This can be one of text, text-image, text-multi, image-text.
tag_field: The field in the tag collection to use for tagging.
tag_vector_field: vector field in the tag collection, used for matching the vectors to tag.
alias: The alias of the tags. Defaults to 'default'
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
number_of_tags: The number of tags to retrieve.
include_tag_vector: Whether to include the one hot encoded tag vector.
refresh: If True, Re-tags from scratch.
hub_username: The username of the hub account.
hub_api_key: The API key of the hub account.
store_to_pipeline: Whether to store the encoders to pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/tag_job',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				tag_collection_name=tag_collection_name, 
				field=field, 
				encoder_task=encoder_task, 
				tag_field=tag_field, 
				tag_vector_field=tag_vector_field, 
				alias=alias, 
				metric=metric, 
				number_of_tags=number_of_tags, 
				include_tag_vector=include_tag_vector, 
				refresh=refresh, 
				hub_username=hub_username, 
				hub_api_key=hub_api_key, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def text_chunking(self, collection_name, text_field, chunk_field, insert_results_to_seperate_collection_name, refresh=True, store_to_pipeline=True, **kwargs):
		"""Chunk a text field
Split text into separate sentences. Encode each sentence to create chunkvectors.
These are stored as _chunkvector_. The chunk field created is `field` + _chunk_.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
text_field: Text field to chunk
chunk_field: Whats the field that the text chunks will belong in
refresh: Whether to refresh the whole collection and re-encode all to vectors
insert_results_to_seperate_collection_name: If specified the chunks will be inserted into a seperate collection. Default is None which means no seperate collection.
store_to_pipeline: Whether to store the encoder to the chunking pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/text_chunking',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				text_field=text_field, 
				chunk_field=chunk_field, 
				refresh=refresh, 
				insert_results_to_seperate_collection_name=insert_results_to_seperate_collection_name, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def text_chunking_encoder(self, collection_name, text_field, chunk_field, insert_results_to_seperate_collection_name, encoder_task="text", refresh=True, store_to_pipeline=True, **kwargs):
		"""Chunk a text field and encode the chunks
Split text into separate sentences. Encode each sentence to create chunkvectors.
These are stored as \_chunkvector\_. The chunk field created is `field` + \_chunk\_.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
text_field: Text field to chunk
chunk_field: Whats the field that the text chunks will belong in
encoder_task: Encoder that is used to turn the text chunks into vectors
refresh: Whether to refresh the whole collection and re-encode all to vectors
insert_results_to_seperate_collection_name: If specified the chunks will be inserted into a seperate collection. Default is None which means no seperate collection.
store_to_pipeline: Whether to store the encoder to the chunking pipeline

"""
		return requests.post(
			url=self.url+'/collection/job/text_chunking_encoder',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				text_field=text_field, 
				chunk_field=chunk_field, 
				encoder_task=encoder_task, 
				refresh=refresh, 
				insert_results_to_seperate_collection_name=insert_results_to_seperate_collection_name, 
				store_to_pipeline=store_to_pipeline, 
				))

	@retry()
	@return_curl_or_response('json')
	def process_pdf(self, collection_name, file_url, filename, **kwargs):
		"""Process pdf
Insert a PDF into Vector AI.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: What collection to insert the PDF into
file_url: The file url blob
filename: The name of the PDF file.

"""
		return requests.post(
			url=self.url+'/collection/job/process_pdf',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				file_url=file_url, 
				filename=filename, 
				))

	@retry()
	@return_curl_or_response('json')
	def process_doc(self, collection_name, file_url, filename, **kwargs):
		"""Process doc or docx
Insert a word doc or docx file into Vector AI
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: What collection to insert the word doc into
file_url: The file url blob
filename: The name of the Doc or DocX file

"""
		return requests.post(
			url=self.url+'/collection/job/process_doc',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				file_url=file_url, 
				filename=filename, 
				))

	@retry()
	@return_curl_or_response('json')
	def copy_collection_from_another_user(self, collection_name, source_collection_name, source_username, source_api_key, **kwargs):
		"""Copy a collection from another user's projects into your project
Copy a collection from another user's projects into your project. This is considered a project job
Args
========
collection_name: Collection to copy into
username: Your username
api_key: Your api key to access the username
source_collection_name: Collection to copy frpm
source_username: Source username of whom the collection belongs to
source_api_key: Api key to access the source username

"""
		return requests.post(
			url=self.url+'/project/copy_collection_from_another_user',
			json=dict(
				collection_name=collection_name, 
				username=self.username,
				api_key=self.api_key,
				source_collection_name=source_collection_name, 
				source_username=source_username, 
				source_api_key=source_api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def chunk_search(self, collection_name, chunk_field, vector, search_fields, chunk_scoring="max", page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, chunk_page=1, chunk_page_size=3, **kwargs):
		"""Vector Similarity Search on Chunks.
Chunk Search allows one to search through chunks inside a document. The major difference
between chunk search and normal search in Vector AI is that it relies on the `_chunkvector_`
field.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
chunk_field: Field that the array of chunked documents are.
chunk_scoring: Scoring method for determining for ranking between document chunks.
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
asc: Whether to sort results by ascending or descending order
vector: Vector, a list/array of floats that represents a piece of data
search_fields: Vector fields to search against
chunk_page: Page of the chunk results
chunk_page_size: Size of each page of chunk results

"""
		return requests.post(
			url=self.url+'/collection/chunk_search',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				chunk_field=chunk_field, 
				chunk_scoring=chunk_scoring, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				vector=vector, 
				search_fields=search_fields, 
				chunk_page=chunk_page, 
				chunk_page_size=chunk_page_size, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_chunk_search(self, collection_name, chunk_field, multivector_query, chunk_scoring="max", page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, chunk_page=1, chunk_page_size=3, **kwargs):
		"""Advanced Vector Similarity Search on Chunks. Support for multiple vectors, vector weightings, facets and filtering
Advanced Chunk Vector Search. Search with a multiple chunkvectors for the most similar documents.

Advanced chunk search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
chunk_field: Field that the array of chunked documents are.
chunk_scoring: Scoring method for determining for ranking between document chunks.
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
asc: Whether to sort results by ascending or descending order
multivector_query: Query for advance search that allows for multiple vector and field querying
chunk_page: Page of the chunk results
chunk_page_size: Size of each page of chunk results

"""
		return requests.post(
			url=self.url+'/collection/advanced_chunk_search',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				chunk_field=chunk_field, 
				chunk_scoring=chunk_scoring, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				multivector_query=multivector_query, 
				chunk_page=chunk_page, 
				chunk_page_size=chunk_page_size, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_multistep_chunk_search(self, collection_name, chunk_field, first_step_multivector_query, chunk_step_multivector_query, chunk_scoring="max", page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, first_step_page=1, first_step_page_size=20, **kwargs):
		"""Vector Similarity Search on Chunks.
Advanced Multistep chunk search involves a simple search followed by chunk search.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
chunk_field: Field that the array of chunked documents are.
chunk_scoring: Scoring method for determining for ranking between document chunks.
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
asc: Whether to sort results by ascending or descending order
first_step_multivector_query: Query for advance search that allows for multiple vector and field querying
chunk_step_multivector_query: Query for advance search that allows for multiple vector and field querying
first_step_page: Page of the results
first_step_page_size: Size of each page of results

"""
		return requests.post(
			url=self.url+'/collection/advanced_multistep_chunk_search',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				chunk_field=chunk_field, 
				chunk_scoring=chunk_scoring, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				first_step_multivector_query=first_step_multivector_query, 
				chunk_step_multivector_query=chunk_step_multivector_query, 
				first_step_page=first_step_page, 
				first_step_page_size=first_step_page_size, 
				))

	@retry()
	@return_curl_or_response('json')
	def id_lookup_joined(self, doc_id, join_query={}, **kwargs):
		"""Look up a document by its id with joins
Look up a document by its id with joins.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
join_query: Join query
doc_id: ID of a Document

"""
		return requests.post(
			url=self.url+'/collection/id_lookup_joined',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				join_query=join_query, 
				doc_id=doc_id, 
				))

	@retry()
	@return_curl_or_response('json')
	def join_collections(self, joined_collection_name, join_query={}, **kwargs):
		"""Join collections with a query
Perform a join query on a whole collection and write the results to a new collection. We currently only support left joins.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
join_query: Join query
joined_collection_name: Name of the new collection that contains the joined results

"""
		return requests.post(
			url=self.url+'/collection/join_collections',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				join_query=join_query, 
				joined_collection_name=joined_collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def publish_aggregation(self, source_collection, dest_collection, aggregation_name, description, aggregation_query, date_field="insert_date_", refresh_time="160s", start_immediately=True, **kwargs):
		"""Publishes your aggregation query to a new collection
Publish and schedules your aggregation query and saves it to a new collection.
This new collection is just like any other collection and you can read, filter and aggregate it.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
source_collection: The collection where the data to aggregate comes from
dest_collection: The name of collection of where the data will be aggregated to
aggregation_name: The name for the published scheduled aggregation
description: The description for the published scheduled aggregation
aggregation_query: The aggregation query to schedule
date_field: The date field to check whether there is new data coming in
refresh_time: How often should the aggregation check for new data
start_immediately: Whether to start the published aggregation immediately

"""
		return requests.post(
			url=self.url+'/collection/publish_aggregation',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				source_collection=source_collection, 
				dest_collection=dest_collection, 
				aggregation_name=aggregation_name, 
				description=description, 
				aggregation_query=aggregation_query, 
				date_field=date_field, 
				refresh_time=refresh_time, 
				start_immediately=start_immediately, 
				))

	@retry()
	@return_curl_or_response('json')
	def delete_published_aggregation(self,aggregation_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/delete_published_aggregation',
			params=dict(
				aggregation_name=aggregation_name, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def start_aggregation(self,aggregation_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/start_aggregation',
			params=dict(
				aggregation_name=aggregation_name, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def stop_aggregation(self,aggregation_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/stop_aggregation',
			params=dict(
				aggregation_name=aggregation_name, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def vector_aggregation(self, source_collection, dest_collection, source_to_dest_fields_mapping, vector_fields, aggregation_type="mean", refresh=True, **kwargs):
		"""Aggregate vectors from one collection into another published aggregation collection
This is useful for getting vectors of a category. e.g. You have "product\_description\_vector\_" and you want the vector for a brand samsung. The "samsung" brand's vector can be the aggregate of all the samsung "product\_description\_vector\_".
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
source_collection: The collection where the data to aggregate comes from
dest_collection: The collection that a scheduled aggregation is creating
source_to_dest_fields_mapping: The collection that a scheduled aggregation is creating
vector_fields: Vector fields to aggregate to form 1 aggregated vector for each split the groupby creates
aggregation_type: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
refresh: Whether to refresh the aggregation and recalculate the vectors for every single groupby

"""
		return requests.post(
			url=self.url+'/collection/vector_aggregation',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				source_collection=source_collection, 
				dest_collection=dest_collection, 
				source_to_dest_fields_mapping=source_to_dest_fields_mapping, 
				vector_fields=vector_fields, 
				aggregation_type=aggregation_type, 
				refresh=refresh, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_array_field(self,array_fields, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_array_field',
			params=dict(
				array_fields=array_fields, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_array(self,array_field, array, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_array',
			params=dict(
				array_field=array_field, 
				array=array, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_multiple_arrays(self, collection_name, multiarray_query, **kwargs):
		"""Encode multiple arrays into vectors.
Encode Multiple arrays
Multiarray query is in the format: 

    {
        "array_1": {"array": ["YES"], "field": "sample_array"},
        "array_2": {"array": ["NO"], "field": "sample_array_2"},
    }
This will then return 
    
    {
        "array_1": [1e-7, 1],
        "array_2": [1, 1e-7]
    }

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
multiarray_query: List of array fields

"""
		return requests.post(
			url=self.url+'/collection/encode_multiple_arrays',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				multiarray_query=multiarray_query, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_array(self,array_field, array, collection_name, search_fields, search_history_id, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, keep_search_history=True, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, **kwargs):
		return requests.get(
			url=self.url+'/collection/search_with_array',
			params=dict(
				array_field=array_field, 
				array=array, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				search_fields=search_fields, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				search_history_id=search_history_id, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_dictionary_field(self,dictionary_fields, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_dictionary_field',
			params=dict(
				dictionary_fields=dictionary_fields, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_dictionary(self, collection_name, dictionary, dictionary_field, **kwargs):
		"""Encode an dictionary into a vector
For example: a dictionary that represents a **person's characteristics visiting a store, field "person_characteristics"**:

    {"height":180, "age":40, "weight":70}

    -> <Encode the dictionary to vector> ->

| height | age | weight | purchases | visits |
|--------|-----|--------|-----------|--------|
| 180    | 40  | 70     | 0         | 0      |

    dictionary vector: [180, 40, 70, 0, 0]
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
dictionary: A dictionary to encode into vectors
dictionary_field: The dictionary field that encoding of the dictionary is trained on

"""
		return requests.post(
			url=self.url+'/collection/encode_dictionary',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				dictionary=dictionary, 
				dictionary_field=dictionary_field, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_dictionary(self, collection_name, search_fields, search_history_id, dictionary, dictionary_field, page_size=20, page=1, approx=0, sum_fields=True, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, keep_search_history=False, **kwargs):
		"""Search a dictionary field with a dictionary using Vector Search
Vector similarity search with a dictionary directly.

For example: a dictionary that represents a **person's characteristics visiting a store, field "person_characteristics"**:

    {"height":180, "age":40, "weight":70}

    -> <Encode the dictionary to vector> ->

| height | age | weight | purchases | visits |
|--------|-----|--------|-----------|--------|
| 180    | 40  | 70     | 0         | 0      |

    dictionary vector: [180, 40, 70, 0, 0]

    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
search_fields: Vector fields to search against
page_size: Size of each page of results
page: Page of the results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
hundred_scale: Whether to scale up the metric by 100
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
search_history_id: Search history ID of the collection.
dictionary: A dictionary to encode into vectors
dictionary_field: The dictionary field that encoding of the dictionary is trained on

"""
		return requests.post(
			url=self.url+'/collection/search_with_dictionary',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				search_fields=search_fields, 
				page_size=page_size, 
				page=page, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				search_history_id=search_history_id, 
				dictionary=dictionary, 
				dictionary_field=dictionary_field, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_fields_to_vector(self, collection_name, vector_name, selected_fields, **kwargs):
		"""Encode all selected fields for a collection into vectors
Within a collection encode the specified fields in every document into vectors.

For example: we choose the fields ["height", "age", "weight"]
    document 1 field: {"height":180, "age":40, "weight":70, "purchases":20, "visits": 12}

    document 2 field: {"height":160, "age":32, "weight":50, "purchases":10, "visits": 24}

    -> <Encode the fields to vectors> ->

| height | age | weight |
|--------|-----|--------|
| 180    | 40  | 70     | 
| 160    | 32  | 50     | 

    document 1 vector: {"person_characteristics_vector_": [180, 40, 70]}

    document 2 vector: {"person_characteristics_vector_": [160, 32, 50]}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vector_name: The name of the vector that the fields turn into
selected_fields: The fields to turn into vectors

"""
		return requests.post(
			url=self.url+'/collection/encode_fields_to_vector',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector_name=vector_name, 
				selected_fields=selected_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_fields(self, collection_name, document, vector_name, **kwargs):
		"""Encode fields into a vector
For example: we choose the fields ["height", "age", "weight"]
    document field: {"height":180, "age":40, "weight":70, "purchases":20, "visits": 12}

    -> <Encode the fields to vectors> ->

| height | age | weight |
|--------|-----|--------|
| 180    | 40  | 70     |

    document vector: {"person_characteristics_vector_": [180, 40, 70]}

    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document: A document to encode into vectors
vector_name: The name of the vector that the fields turn into

"""
		return requests.post(
			url=self.url+'/collection/encode_fields',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				vector_name=vector_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_fields(self, collection_name, search_fields, search_history_id, document, selected_fields, vector_name, page_size=20, page=1, approx=0, sum_fields=True, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, keep_search_history=False, **kwargs):
		"""Search with fields with a document using Vector Search
Vector similarity search with fields directly.

For example: we choose the fields ["height", "age", "weight"]
    document field: {"height":180, "age":40, "weight":70, "purchases":20, "visits": 12}

    -> <Encode the fields to vectors> ->

| height | age | weight |
|--------|-----|--------|
| 180    | 40  | 70     |

    document dictionary vector: {"person_characteristics_vector_": [180, 40, 70]}

    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
search_fields: Vector fields to search against
page_size: Size of each page of results
page: Page of the results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
hundred_scale: Whether to scale up the metric by 100
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
search_history_id: Search history ID of the collection.
document: A document to encode into vectors
selected_fields: The fields to turn into vectors
vector_name: A name to call the vector that the fields turn into

"""
		return requests.post(
			url=self.url+'/collection/search_with_fields',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				search_fields=search_fields, 
				page_size=page_size, 
				page=page, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				hundred_scale=hundred_scale, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				search_history_id=search_history_id, 
				document=document, 
				selected_fields=selected_fields, 
				vector_name=vector_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def combine_vectors(self,vector_fields, vector_name, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/combine_vectors',
			params=dict(
				vector_fields=vector_fields, 
				vector_name=vector_name, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_vector_mappings(self,collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/collection_vector_mappings',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster(self,vector_field, collection_name, n_clusters=0, gpu=True, refresh=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/cluster',
			params=dict(
				vector_field=vector_field, 
				n_clusters=n_clusters, 
				gpu=gpu, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster_aggregate(self, collection_name, aggregation_query, filters=[], page_size=20, page=1, asc=False, flatten=True, **kwargs):
		"""Aggregate every cluster in a collection
Takes an aggregation query and gets the aggregate of each cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /cluster.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
filters: Query for filtering the search results
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 

"""
		return requests.post(
			url=self.url+'/collection/cluster_aggregate',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				filters=filters, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster_facets(self,collection_name, facets_fields=[], page_size=1000, page=1, asc=False, date_interval="monthly", **kwargs):
		return requests.get(
			url=self.url+'/collection/cluster_facets',
			params=dict(
				facets_fields=facets_fields, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				date_interval=date_interval, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster_centroids(self,vector_field, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/cluster_centroids',
			params=dict(
				vector_field=vector_field, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster_centroid_documents(self,vector_field, collection_name, metric="cosine", include_vector=False, page=1, page_size=20, **kwargs):
		return requests.get(
			url=self.url+'/collection/cluster_centroid_documents',
			params=dict(
				vector_field=vector_field, 
				metric=metric, 
				include_vector=include_vector, 
				page=page, 
				page_size=page_size, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster(self,vector_field, collection_name, alias="default", n_clusters=0, n_iter=10, n_init=5, gpu=True, refresh=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/advanced_cluster',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				n_clusters=n_clusters, 
				n_iter=n_iter, 
				n_init=n_init, 
				gpu=gpu, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster_aggregate(self, collection_name, aggregation_query, vector_field, alias, filters=[], page_size=20, page=1, asc=False, flatten=True, **kwargs):
		"""Aggregate every cluster in a collection
Takes an aggregation query and gets the aggregate of each cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /advanced_cluster.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
filters: Query for filtering the search results
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 
vector_field: Clustered vector field
alias: Alias of a cluster

"""
		return requests.post(
			url=self.url+'/collection/advanced_cluster_aggregate',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				filters=filters, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				vector_field=vector_field, 
				alias=alias, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster_facets(self,vector_field, collection_name, alias="default", facets_fields=[], page_size=1000, page=1, asc=False, date_interval="monthly", **kwargs):
		return requests.get(
			url=self.url+'/collection/advanced_cluster_facets',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				facets_fields=facets_fields, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				date_interval=date_interval, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster_centroids(self,vector_field, collection_name, alias="default", **kwargs):
		return requests.get(
			url=self.url+'/collection/advanced_cluster_centroids',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster_centroid_documents(self,vector_field, collection_name, alias="default", metric="cosine", include_vector=False, page=1, page_size=20, **kwargs):
		return requests.get(
			url=self.url+'/collection/advanced_cluster_centroid_documents',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				metric=metric, 
				include_vector=include_vector, 
				page=page, 
				page_size=page_size, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster_search(self, collection_name, multivector_query, vector_field, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, alias="default", **kwargs):
		"""Advanced Vector Similarity Search on Clusters. 
Only can be used after a vector field has been clustered with /advanced_cluster. Perform advanced_search on each cluster
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
multivector_query: Query for advance search that allows for multiple vector and field querying
vector_field: Vector field to perform clustering on
alias: Alias is used to name a cluster

"""
		return requests.post(
			url=self.url+'/collection/advanced_cluster_search',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				multivector_query=multivector_query, 
				vector_field=vector_field, 
				alias=alias, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_post_cluster(self, collection_name, multivector_query, cluster_vector_field, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, n_clusters=0, n_init=5, n_iter=10, return_as_clusters=False, **kwargs):
		"""Performs Clustering on Top X search results
This will first perform an advanced search and then cluster the top X (page_size) search results.
Results are returned as such: 
Once you have the clusters: 

```
Cluster 0: [A, B, C]
Cluster 1: [D, E]
Cluster 2: [F, G]
Cluster 3: [H, I]
```
(Note, each cluster is ordered by highest to lowest search score.

This intermediately returns:

```
results_batch_1: [A, H, F, D] (ordered by highest search score)
results_batch_2: [G, E, B, I] (ordered by highest search score)
results_batch_3: [C]
```

This then returns the final results:

```
results: [A, H, F, D, G, E, B, I, C]
```
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
multivector_query: Query for advance search that allows for multiple vector and field querying
cluster_vector_field: Vector field to perform clustering on
n_clusters: Number of clusters
n_init: Number of runs to run with different centroid seeds
n_iter: Number of iterations in each run
return_as_clusters: If True, return as clusters as opposed to results list

"""
		return requests.post(
			url=self.url+'/collection/advanced_search_post_cluster',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				multivector_query=multivector_query, 
				cluster_vector_field=cluster_vector_field, 
				n_clusters=n_clusters, 
				n_init=n_init, 
				n_iter=n_iter, 
				return_as_clusters=return_as_clusters, 
				))

	@retry()
	@return_curl_or_response('json')
	def insert_cluster_centroids(self, collection_name, cluster_centers, vector_field, alias="default", job=False, job_metric="cosine", **kwargs):
		"""Insert cluster centroids
Insert your own cluster centroids for it to be used in approximate search settings and cluster aggregations.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
cluster_centers: Cluster centers with the key being the index number
vector_field: Clustered vector field
alias: Alias is used to name a cluster
job: Whether to run a job where each document is assigned a cluster from the cluster_center
job_metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']

"""
		return requests.post(
			url=self.url+'/collection/insert_cluster_centroids',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				cluster_centers=cluster_centers, 
				vector_field=vector_field, 
				alias=alias, 
				job=job, 
				job_metric=job_metric, 
				))

	@retry()
	@return_curl_or_response('json')
	def dimensionality_reduce(self, collection_name, vectors, vector_field, alias="default", n_components=1, **kwargs):
		"""Reduces the dimension of a list of vectors
Reduce the dimensions of a list of vectors you input into a desired dimension. 

This can only reduce to dimensions less than or equal to the n_components that the dimensionality reduction model is trained on.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vectors: Vectors to perform dimensionality reduction on
vector_field: Vector field to perform dimensionality reduction on
alias: Alias of the dimensionality reduced vectors
n_components: The size/length to reduce the vector down to.

"""
		return requests.post(
			url=self.url+'/collection/dimensionality_reduce',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vectors=vectors, 
				vector_field=vector_field, 
				alias=alias, 
				n_components=n_components, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_text_field(self,text_field, collection_name, refresh=True, alias="default", **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_text_field',
			params=dict(
				text_field=text_field, 
				refresh=refresh, 
				alias=alias, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_text(self,text, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_text',
			params=dict(
				text=text, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_encode_text(self,texts, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/bulk_encode_text',
			params=dict(
				texts=texts, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_text(self, collection_name, text, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Search text fields with text using Vector Search
Vector similarity search with text directly.

For example: "product_description" represents the description of a product:

    "AirPods deliver effortless, all-day audio on the go. And AirPods Pro bring Active Noise Cancellation to an in-ear headphone — with a customisable fit"

    -> <Encode the text to vector> ->

    i.e. text vector, "product_description_vector_": [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
text: Text to encode into vector and vector search with
search_fields: Vector fields to search against

"""
		return requests.post(
			url=self.url+'/collection/search_with_text',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				text=text, 
				search_fields=search_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_image_field(self,image_field, collection_name, alias="default", refresh=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_image_field',
			params=dict(
				image_field=image_field, 
				alias=alias, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_image(self,image_url, model_url, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_image',
			params=dict(
				image_url=image_url, 
				model_url=model_url, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_encode_image(self,image_urls, model_url, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/bulk_encode_image',
			params=dict(
				image_urls=image_urls, 
				model_url=model_url, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_image(self, collection_name, image_url, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Search an image field with image using Vector Search
Vector similarity search with an image directly.

_note: image has to be stored somewhere and be provided as image_url, a url that stores the image_

For example: an image_url represents an image of a celebrity:

    "https://www.celebrity_images.com/brad_pitt.png"

    -> <Encode the image to vector> ->

    image vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
image_url: The image url of an image to encode into a vector
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url=self.url+'/collection/search_with_image',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				image_url=image_url, 
				model_url=model_url, 
				search_fields=search_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_image_upload(self, collection_name, image, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Search an image field with uploaded image using Vector Search
Vector similarity search with an uploaded image directly.

_note: image has to be sent as a base64 encoded string_

For example: an image represents an image of a celebrity:

    "https://www.celebrity_images.com/brad_pitt.png"

    -> <Encode the image to vector> ->

    image vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
image: Image represented as a base64 encoded string
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url=self.url+'/collection/search_with_image_upload',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				image=image, 
				model_url=model_url, 
				search_fields=search_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_audio_field(self,audio_field, collection_name, refresh=True, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_audio_field',
			params=dict(
				audio_field=audio_field, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_audio(self,audio_url, model_url, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/encode_audio',
			params=dict(
				audio_url=audio_url, 
				model_url=model_url, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def bulk_encode_audio(self,audio_urls, collection_name, **kwargs):
		return requests.get(
			url=self.url+'/collection/bulk_encode_audio',
			params=dict(
				audio_urls=audio_urls, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_audio(self, collection_name, audio_url, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Search an audio field with audio using Vector Search
Vector similarity search with an audio directly.

_note: audio has to be stored somewhere and be provided as audio_url, a url that stores the audio_

For example: an audio_url represents sounds that a pokemon make:

    "https://play.pokemonshowdown.com/audio/cries/pikachu.mp3"

    -> <Encode the audio to vector> ->

    audio vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]

    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
audio_url: The audio url of an audio to encode into a vector
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url=self.url+'/collection/search_with_audio',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				audio_url=audio_url, 
				model_url=model_url, 
				search_fields=search_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_audio_upload(self, collection_name, audio, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, keep_search_history=False, **kwargs):
		"""Advanced Search audio fields with uploaded audio using Vector Search
Vector similarity search with an uploaded audio directly.

_note: audio has to be sent as a base64 encoded string_

For example: an audio represents sounds that a pokemon make:

    "https://play.pokemonshowdown.com/audio/cries/pikachu.mp3"

    -> <Encode the audio to vector> ->

    audio vector: [0.794617772102356, 0.3581121861934662, 0.21113917231559753, 0.24878688156604767, 0.9741804003715515 ...]
    -> <Vector Search> ->

    Search Results: {...}
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
page: Page of the results
page_size: Size of each page of results
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
facets: Fields to include in the facets, if [] then all
min_score: Minimum score for similarity metric
include_fields: Fields to include in the search results, empty array/list means all fields.
include_vector: Include vectors in the search results
include_count: Include count in the search results
include_facets: Include facets in the search results
hundred_scale: Whether to scale up the metric by 100
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
keep_search_history: Whether to store the history of search or not
audio: Audio represented as a base64 encoded string
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url=self.url+'/collection/search_with_audio_upload',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				page=page, 
				page_size=page_size, 
				approx=approx, 
				sum_fields=sum_fields, 
				metric=metric, 
				filters=filters, 
				facets=facets, 
				min_score=min_score, 
				include_fields=include_fields, 
				include_vector=include_vector, 
				include_count=include_count, 
				include_facets=include_facets, 
				hundred_scale=hundred_scale, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				keep_search_history=keep_search_history, 
				audio=audio, 
				model_url=model_url, 
				search_fields=search_fields, 
				))

	@retry()
	@return_curl_or_response('json')
	def text_chunking(self, collection_name, text_field, chunk_field, insert_results_to_seperate_collection_name, refresh=True, insert_results=True, return_processed_documents=False, **kwargs):
		"""Chunking a text field in a collection.
Chunking a text field in a collection. e.g. a paragraph text field to sentence chunks
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
text_field: Text field to chunk
chunk_field: Whats the field that the text chunks will belong in
refresh: Whether to refresh the whole collection and re-encode all to vectors
insert_results: Whether to insert the processed document chunks into the collection.
insert_results_to_seperate_collection_name: If specified the chunks will be inserted into a seperate collection. Default is None which means no seperate collection.
return_processed_documents: Whether to return the processed documents.

"""
		return requests.post(
			url=self.url+'/collection/text_chunking',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				text_field=text_field, 
				chunk_field=chunk_field, 
				refresh=refresh, 
				insert_results=insert_results, 
				insert_results_to_seperate_collection_name=insert_results_to_seperate_collection_name, 
				return_processed_documents=return_processed_documents, 
				))

	@retry()
	@return_curl_or_response('json')
	def tag(self, data, tag_collection_name, encoder, tag_field, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", filters=[], min_score=None, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, **kwargs):
		"""Add tagging
Tag
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
data: Image Url or text or any data suited for the encoder
tag_collection_name: Name of the collection you want to tag
encoder: Which encoder to use.
tag_field: The field used to tag in a collection. If None, automatically uses the one stated in the encoder.
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
page_size: Size of each page of results
page: Page of the results
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
min_score: Minimum score for similarity metric
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order

"""
		return requests.post(
			url=self.url+'/collection/tag',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				data=data, 
				tag_collection_name=tag_collection_name, 
				encoder=encoder, 
				tag_field=tag_field, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				filters=filters, 
				min_score=min_score, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def post_cluster_tag(self, data, tag_collection_name, encoder, tag_field, cluster_vector_field, n_clusters, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", filters=[], min_score=None, include_search_relevance=False, search_relevance_cutoff_aggressiveness=1, asc=False, n_iter=10, n_init=5, **kwargs):
		"""Post cluster tag.
Post cluster tag.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
data: Image Url or text or any data suited for the encoder
tag_collection_name: Name of the collection you want to tag
encoder: Which encoder to use.
tag_field: The field used to tag in a collection. If None, automatically uses the one stated in the encoder.
approx: Used for approximate search
sum_fields: Whether to sum the multiple vectors similarity search score as 1 or seperate
page_size: Size of each page of results
page: Page of the results
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
filters: Query for filtering the search results
min_score: Minimum score for similarity metric
include_search_relevance: Whether to calculate a search_relevance cutoff score to flag relevant and less relevant results
search_relevance_cutoff_aggressiveness: How aggressive the search_relevance cutoff score is (higher value the less results will be relevant)
asc: Whether to sort results by ascending or descending order
cluster_vector_field: The field to cluster on.
n_clusters: Number of clusters to be specified.
n_iter: Number of iterations in each run
n_init: Number of runs to run with different centroid seeds

"""
		return requests.post(
			url=self.url+'/collection/post_cluster_tag',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				data=data, 
				tag_collection_name=tag_collection_name, 
				encoder=encoder, 
				tag_field=tag_field, 
				approx=approx, 
				sum_fields=sum_fields, 
				page_size=page_size, 
				page=page, 
				metric=metric, 
				filters=filters, 
				min_score=min_score, 
				include_search_relevance=include_search_relevance, 
				search_relevance_cutoff_aggressiveness=search_relevance_cutoff_aggressiveness, 
				asc=asc, 
				cluster_vector_field=cluster_vector_field, 
				n_clusters=n_clusters, 
				n_iter=n_iter, 
				n_init=n_init, 
				))

	@retry()
	@return_curl_or_response('json')
	def tag_collection_from_vectors(self, collection_name, vector_field, tag_collection_name, tag_field="tag", tag_vector_field="tag_vector_", metric="cosine", alias="default", number_of_tags=5, include_tag_vector=True, pad_vector_length=100, refresh=True, return_tagged_documents=True, **kwargs):
		"""Add tagging
Tag vectors
   
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
vector_field: vector field from the source collection to tag on
tag_collection_name: Name of the collection you are retrieving the tags from
tag_field: The field in the tag collection to use for tagging.
tag_vector_field: vector field in the tag collection, used for matching the vectors to tag.
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
alias: The alias of the tags. Defaults to 'default'
number_of_tags: The number of tags to retrieve.
include_tag_vector: Whether to include the one hot encoded tag vector.
pad_vector_length: Whether to pad the vector length of the one hot encoded array.
refresh: If True, retags the whole collection.
return_tagged_documents: If True, returns the original documents with tags.

"""
		return requests.post(
			url=self.url+'/collection/tag_collection_from_vectors',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector_field=vector_field, 
				tag_collection_name=tag_collection_name, 
				tag_field=tag_field, 
				tag_vector_field=tag_vector_field, 
				metric=metric, 
				alias=alias, 
				number_of_tags=number_of_tags, 
				include_tag_vector=include_tag_vector, 
				pad_vector_length=pad_vector_length, 
				refresh=refresh, 
				return_tagged_documents=return_tagged_documents, 
				))

	@retry()
	@return_curl_or_response('json')
	def tag_documents(self, tag_collection_name, vector_field, documents={}, tag_field="tag", tag_vector_field="tag_vector_", alias="default", metric="cosine", number_of_tags=5, field="", include_tag_vector=True, pad_vector_length=100, **kwargs):
		"""Tag documents.
Tag documents
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
tag_collection_name: Name of the collection you are retrieving the tags from
tag_field: The field in the tag collection to use for tagging.
tag_vector_field: vector field in the tag collection, used for matching the vectors to tag.
alias: The alias of the tags. Defaults to 'default'
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
number_of_tags: The number of tags to retrieve.
field: The field in the source collection to be tagged.
vector_field: vector field from the source collection to tag on
include_tag_vector: Whether to include the one hot encoded tag vector.
pad_vector_length: Whether to pad the vector length of the one hot encoded array.

"""
		return requests.post(
			url=self.url+'/collection/tag_documents',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				documents=documents, 
				tag_collection_name=tag_collection_name, 
				tag_field=tag_field, 
				tag_vector_field=tag_vector_field, 
				alias=alias, 
				metric=metric, 
				number_of_tags=number_of_tags, 
				field=field, 
				vector_field=vector_field, 
				include_tag_vector=include_tag_vector, 
				pad_vector_length=pad_vector_length, 
				))

	@retry()
	@return_curl_or_response('json')
	def store_taggers_pipeline(self, collection_name, taggers, **kwargs):
		"""Store multiple tagger pipelines
Store pipeline for taggers.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
taggers: Taggers contain metadata to
encode and then use a specific collection to get data.

    {"field": field, "vector_field": vector_field, "tag_field": tag_field, 
    "tag_vector_field": tag_vector_field, "number_of_tags": number_of_tags,
    "alias": alias, "metric": metric}

    

"""
		return requests.post(
			url=self.url+'/collection/store_taggers_pipeline',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				taggers=taggers, 
				))

	@retry()
	@return_curl_or_response('json')
	def tag_documents_from_hub(self, tag_collection_name, vector_field, hub_username, hub_api_key, documents={}, tag_field="tag", tag_vector_field="tag_vector_", alias="default", metric="cosine", number_of_tags=5, field="", include_tag_vector=True, pad_vector_length=100, **kwargs):
		"""Add tagging from the Tag Hub.
Tag documents from hub API
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
tag_collection_name: Name of the collection you are retrieving the tags from
tag_field: The field in the tag collection to use for tagging.
tag_vector_field: vector field in the tag collection, used for matching the vectors to tag.
alias: The alias of the tags. Defaults to 'default'
metric: Similarity Metric, choose from ['cosine', 'l1', 'l2', 'dp']
number_of_tags: The number of tags to retrieve.
field: The field in the source collection to be tagged.
vector_field: vector field from the source collection to tag on
include_tag_vector: Whether to include the one hot encoded tag vector.
pad_vector_length: Whether to pad the vector length of the one hot encoded array.
hub_username: The username of the hub for the tag.
hub_api_key: The api key of the hub for the tag.

"""
		return requests.post(
			url=self.url+'/collection/tag_documents_from_hub',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				documents=documents, 
				tag_collection_name=tag_collection_name, 
				tag_field=tag_field, 
				tag_vector_field=tag_vector_field, 
				alias=alias, 
				metric=metric, 
				number_of_tags=number_of_tags, 
				field=field, 
				vector_field=vector_field, 
				include_tag_vector=include_tag_vector, 
				pad_vector_length=pad_vector_length, 
				hub_username=hub_username, 
				hub_api_key=hub_api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def rank_comparator(self, ranked_list_1, ranked_list_2, **kwargs):
		"""Compare ranks between 2 results list.
Compare the ranks between 2 results list in VecDB
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
ranked_list_1: First ranked List
ranked_list_2: Second ranked list

"""
		return requests.post(
			url=self.url+'/experimentation/rank_comparator',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				ranked_list_1=ranked_list_1, 
				ranked_list_2=ranked_list_2, 
				))

	@retry()
	@return_curl_or_response('json')
	def bias_indicator(self, anchor_documents, documents, metadata_field, vector_field, **kwargs):
		"""Compare bias of documents against anchor documents
Compare bias of documents against anchor documents
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
anchor_documents: Anchor documents to compare other documents against.
documents: Documents to compare against the anchor documents
metadata_field: Field from which the vector was derived
vector_field: Vector field to compare against

"""
		return requests.post(
			url=self.url+'/experimentation/bias_indicator',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				anchor_documents=anchor_documents, 
				documents=documents, 
				metadata_field=metadata_field, 
				vector_field=vector_field, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster_comparator(self, collection_name, cluster_field, cluster_value, vector_field, alias, **kwargs):
		"""Compare clusters
Compare the clusters for cluster comparator
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: the name of the collection
cluster_field: the cluster field
cluster_value: the cluster values by which to compare on
vector_field: The vector field that has been clustered
alias: The alias of the vector field

"""
		return requests.post(
			url=self.url+'/experimentation/cluster_comparator',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				cluster_field=cluster_field, 
				cluster_value=cluster_value, 
				vector_field=vector_field, 
				alias=alias, 
				))

