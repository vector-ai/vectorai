# This python file is auto-generated. Please do not edit.
import requests
import requests
from vectorai.api.utils import retry, return_curl_or_response


class ViAPIClient:
	def __init__(self, username, api_key, ):
		self.username = username		
		self.api_key = api_key		

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
			url='https://api.vctr.ai/project/request_api_key',
			json=dict(
				username=self.username,
				email=email, 
				description=description, 
				referral_code=referral_code, 
				**kwargs))

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
			url='https://api.vctr.ai/project/request_read_api_key',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				read_username=read_username, 
				**kwargs))

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
			url='https://api.vctr.ai/project/create_collection',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				collection_schema=collection_schema, 
				**kwargs))

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
			url='https://api.vctr.ai/project/create_collection_from_document',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def _delete_collection(self,collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/delete_collection',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def _list_collections(self,**kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/list_collections',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_stats(self,collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/collection_stats',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_schema(self,collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/collection_schema',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def collection_vector_health(self,collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/collection_vector_health',
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
			url='https://api.vctr.ai/project/add_collection_metadata',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				metadata=metadata, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def collection_metadata(self,collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/collection_metadata',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
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
			url='https://api.vctr.ai/project/copy_collection_from_another_user',
			json=dict(
				collection_name=collection_name, 
				username=self.username,
				api_key=self.api_key,
				source_collection_name=source_collection_name, 
				source_username=source_username, 
				source_api_key=source_api_key, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def job_status(self,job_id, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/project/job_status',
			params=dict(
				job_id=job_id, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def _search(self,vector, collection_name, search_fields, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/search',
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
				))

	@retry()
	@return_curl_or_response('json')
	def search_by_id(self,document_id, collection_name, search_field, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/search_by_id',
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
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_by_ids(self,document_ids, collection_name, search_field, vector_operation="sum", approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/search_by_ids',
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
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_by_positive_negative_ids(self,positive_document_ids, negative_document_ids, collection_name, search_field, vector_operation="sum", approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/search_by_positive_negative_ids',
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
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_positive_negative_ids_as_history(self,vector, positive_document_ids, negative_document_ids, collection_name, search_field, vector_operation="sum", approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/search_with_positive_negative_ids_as_history',
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
				asc=asc, 
				))

	@retry()
	@return_curl_or_response('json')
	def hybrid_search(self,text, vector, collection_name, search_fields, text_fields=[], traditional_weight=0.075, fuzzy=1, join=True, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/hybrid_search',
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
				))

	@retry()
	@return_curl_or_response('json')
	def insert(self, collection_name, document={}, insert_date=True, overwrite=True, update_schema=True, **kwargs):
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

"""
		return requests.post(
			url='https://api.vctr.ai/collection/insert',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				update_schema=update_schema, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def bulk_insert(self, collection_name, documents={}, insert_date=True, overwrite=True, update_schema=True, quick=False, **kwargs):
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

"""
		return requests.post(
			url='https://api.vctr.ai/collection/bulk_insert',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				documents=documents, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				update_schema=update_schema, 
				quick=quick, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def delete_by_id(self,document_id, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/delete_by_id',
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
Delete a document by its id.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document_ids: IDs of documents

"""
		return requests.post(
			url='https://api.vctr.ai/collection/bulk_delete_by_id',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document_ids=document_ids, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def _edit_document(self, collection_name, document_id, edits, insert_date=True, **kwargs):
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
			url='https://api.vctr.ai/collection/edit_document',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document_id=document_id, 
				edits=edits, 
				insert_date=insert_date, 
				**kwargs))

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
			url='https://api.vctr.ai/collection/bulk_edit_document',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				documents=documents, 
				insert_date=insert_date, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def delete_document_fields(self,document_id, fields_to_delete, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/delete_document_fields',
			params=dict(
				document_id=document_id, 
				fields_to_delete=fields_to_delete, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def id(self,document_id, collection_name, include_vector=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/id',
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
			url='https://api.vctr.ai/collection/bulk_id',
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
			url='https://api.vctr.ai/collection/bulk_missing_id',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document_ids=document_ids, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def retrieve_documents(self,collection_name, include_fields=[], cursor=None, page_size=20, sort=[], asc=False, include_vector=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/retrieve_documents',
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
			url='https://api.vctr.ai/collection/random_documents',
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
	def retrieve_documents_with_filters(self, collection_name, include_fields=[], cursor=None, page_size=20, sort=[], asc=False, include_vector=False, filters=[], **kwargs):
		"""Retrieve some documents with filters
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
			url='https://api.vctr.ai/collection/retrieve_documents_with_filters',
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
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def random_documents_with_filters(self, collection_name, seed=10, include_fields=[], page_size=20, include_vector=False, filters=[], **kwargs):
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
			url='https://api.vctr.ai/collection/random_documents_with_filters',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				seed=seed, 
				include_fields=include_fields, 
				page_size=page_size, 
				include_vector=include_vector, 
				filters=filters, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def facets(self,collection_name, facets_fields=[], date_interval="monthly", page_size=1000, page=1, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/facets',
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
			url='https://api.vctr.ai/collection/filters',
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
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_search(self, collection_name, multivector_query, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
multivector_query: Query for advance search that allows for multiple vector and field querying

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_search',
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
				asc=asc, 
				multivector_query=multivector_query, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_by_id(self, collection_name, document_id, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
document_id: ID of a document
search_fields: Vector fields to search against, and the weightings for them.

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_search_by_id',
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
				asc=asc, 
				document_id=document_id, 
				search_fields=search_fields, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_by_ids(self, collection_name, document_ids, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, vector_operation="sum", **kwargs):
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
asc: Whether to sort results by ascending or descending order
document_ids: Document IDs to get recommendations for, and the weightings of each document
search_fields: Vector fields to search against, and the weightings for them.
vector_operation: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_search_by_ids',
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
				asc=asc, 
				document_ids=document_ids, 
				search_fields=search_fields, 
				vector_operation=vector_operation, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_by_positive_negative_ids(self, collection_name, positive_document_ids, negative_document_ids, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, vector_operation="sum", **kwargs):
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
asc: Whether to sort results by ascending or descending order
positive_document_ids: Positive Document IDs to get recommendations for, and the weightings of each document
negative_document_ids: Negative Document IDs to get recommendations for, and the weightings of each document
search_fields: Vector fields to search against, and the weightings for them.
vector_operation: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_search_by_positive_negative_ids',
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
				asc=asc, 
				positive_document_ids=positive_document_ids, 
				negative_document_ids=negative_document_ids, 
				search_fields=search_fields, 
				vector_operation=vector_operation, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_search_with_positive_negative_ids_as_history(self, collection_name, positive_document_ids, negative_document_ids, search_fields, vector, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, vector_operation="sum", **kwargs):
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
asc: Whether to sort results by ascending or descending order
positive_document_ids: Positive Document IDs to get recommendations for, and the weightings of each document
negative_document_ids: Negative Document IDs to get recommendations for, and the weightings of each document
search_fields: Vector fields to search against, and the weightings for them.
vector_operation: Aggregation for the vectors, choose from ['mean', 'sum', 'min', 'max']
vector: Vector, a list/array of floats that represents a piece of data

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_search_with_positive_negative_ids_as_history',
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
				asc=asc, 
				positive_document_ids=positive_document_ids, 
				negative_document_ids=negative_document_ids, 
				search_fields=search_fields, 
				vector_operation=vector_operation, 
				vector=vector, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_hybrid_search(self, collection_name, multivector_query, text, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, text_fields=[], traditional_weight=0.075, fuzzy=1, join=True, **kwargs):
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
asc: Whether to sort results by ascending or descending order
multivector_query: Query for advance search that allows for multiple vector and field querying
text: Text Search Query (not encoded as vector)
text_fields: Text fields to search against
traditional_weight: Multiplier of traditional search. A value of 0.025~0.1 is good.
fuzzy: Fuzziness of the search. A value of 1-3 is good.
join: Whether to consider cases where there is a space in the word. E.g. Go Pro vs GoPro.

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_hybrid_search',
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
				asc=asc, 
				multivector_query=multivector_query, 
				text=text, 
				text_fields=text_fields, 
				traditional_weight=traditional_weight, 
				fuzzy=fuzzy, 
				join=join, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def aggregate(self, collection_name, aggregation_query, page_size=20, page=1, asc=False, flatten=True, **kwargs):
		"""Aggregate a collection
Aggregation/Groupby of a collection using an aggregation query.
The aggregation query is a json body that follows the schema of:

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
- "metrics" is the fields you want to metrics you want to calculate in each of those, every aggregation includes a frequency metric. These are the available metric types: 
    - "avg", "max", "min", "sum", "cardinality"
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 

"""
		return requests.post(
			url='https://api.vctr.ai/collection/aggregate',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				**kwargs))

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
			url='https://api.vctr.ai/collection/publish_aggregation',
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
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def delete_published_aggregation(self,aggregation_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/delete_published_aggregation',
			params=dict(
				aggregation_name=aggregation_name, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def start_aggregation(self,aggregation_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/start_aggregation',
			params=dict(
				aggregation_name=aggregation_name, 
				username=self.username, 
				api_key=self.api_key, 
				))

	@retry()
	@return_curl_or_response('json')
	def stop_aggregation(self,aggregation_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/stop_aggregation',
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
			url='https://api.vctr.ai/collection/vector_aggregation',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				source_collection=source_collection, 
				dest_collection=dest_collection, 
				source_to_dest_fields_mapping=source_to_dest_fields_mapping, 
				vector_fields=vector_fields, 
				aggregation_type=aggregation_type, 
				refresh=refresh, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def id_lookup_joined(self, join_query, doc_id, **kwargs):
		"""Look up a document by its id with joins
Look up a document by its id with joins.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
join_query: 
doc_id: ID of a Document

"""
		return requests.post(
			url='https://api.vctr.ai/collection/id_lookup_joined',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				join_query=join_query, 
				doc_id=doc_id, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def join_collections(self, join_query, joined_collection_name, **kwargs):
		"""Join collections with a query
Perform a join query on a whole collection and write the results to a new collection. We currently only support left joins.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
join_query: 
joined_collection_name: Name of the new collection that contains the joined results

"""
		return requests.post(
			url='https://api.vctr.ai/collection/join_collections',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				join_query=join_query, 
				joined_collection_name=joined_collection_name, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def chunk_search(self, collection_name, chunk_field, vector, search_fields, chunk_scoring="max", page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
		"""Vector Similarity Search on Chunks.
Vector Similarity Search on chunks.

For example: Search with a person's characteristics, who are the most similar (querying the "persons_characteristics_vector" field):

    Query person's characteristics as a vector: 
    [180, 40, 70] representing [height, age, weight]

    Search Results:
    [
        {"name": Adam Levine, "persons_characteristics_vector" : [180, 56, 71]},
        {"name": Brad Pitt, "persons_characteristics_vector" : [180, 56, 65]},
    ...]
    
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

"""
		return requests.post(
			url='https://api.vctr.ai/collection/chunk_search',
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
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_chunk_search(self, collection_name, chunk_field, multivector_query, chunk_scoring="max", page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
		"""Advanced Vector Similarity Search on Chunks. Support for multiple vectors, vector weightings, facets and filtering
Advanced Vector Similarity Search, enables machine learning search with vector search. Search with a multiple vectors for the most similar documents.

For example: Search with a product image and description vectors to find the most similar products by what it looks like and what its described to do.

You can also give weightings of each vector field towards the search, e.g. image\_vector\_ weights 100%, whilst description\_vector\_ 50%.

Advanced search also supports filtering to only search through filtered results and facets to get the overview of products available when a minimum score is set.

    
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

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_chunk_search',
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
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def cluster_aggregate(self, collection_name, aggregation_query, page_size=20, page=1, asc=False, flatten=True, **kwargs):
		"""Aggregate every cluster in a collection
Takes an aggregation query and gets the aggregate of each cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /cluster.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 

"""
		return requests.post(
			url='https://api.vctr.ai/collection/cluster_aggregate',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def cluster_facets(self,collection_name, facets_fields=[], page_size=1000, page=1, asc=False, date_interval="monthly", **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/cluster_facets',
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
			url='https://api.vctr.ai/collection/cluster_centroids',
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
			url='https://api.vctr.ai/collection/cluster_centroid_documents',
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
			url='https://api.vctr.ai/collection/advanced_cluster',
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
	def advanced_cluster_aggregate(self, collection_name, aggregation_query, vector_field, alias, page_size=20, page=1, asc=False, flatten=True, filters=[], **kwargs):
		"""Aggregate every cluster in a collection
Takes an aggregation query and gets the aggregate of each cluster in a collection. This helps you interpret each cluster and what is in them.

Only can be used after a vector field has been clustered with /advanced_cluster.
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
aggregation_query: Aggregation query to aggregate data
page_size: Size of each page of results
page: Page of the results
asc: Whether to sort results by ascending or descending order
flatten: 
vector_field: Clustered vector field
alias: Alias of a cluster
filters: Query for filtering the search results

"""
		return requests.post(
			url='https://api.vctr.ai/collection/advanced_cluster_aggregate',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				aggregation_query=aggregation_query, 
				page_size=page_size, 
				page=page, 
				asc=asc, 
				flatten=flatten, 
				vector_field=vector_field, 
				alias=alias, 
				filters=filters, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster_facets(self,vector_field, collection_name, alias="default", facets_fields=[], page_size=1000, page=1, asc=False, date_interval="monthly", **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/advanced_cluster_facets',
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
			url='https://api.vctr.ai/collection/advanced_cluster_centroids',
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
			url='https://api.vctr.ai/collection/advanced_cluster_centroid_documents',
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
			url='https://api.vctr.ai/collection/insert_cluster_centroids',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				cluster_centers=cluster_centers, 
				vector_field=vector_field, 
				alias=alias, 
				job=job, 
				job_metric=job_metric, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def dimensionality_reduction(self,vector_field, collection_name, alias="default", n_components=0, gpu=True, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/dimensionality_reduction',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				n_components=n_components, 
				gpu=gpu, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
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
			url='https://api.vctr.ai/collection/dimensionality_reduce',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vectors=vectors, 
				vector_field=vector_field, 
				alias=alias, 
				n_components=n_components, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def encode_array_field(self,array_fields, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/encode_array_field',
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
			url='https://api.vctr.ai/collection/encode_array',
			params=dict(
				array_field=array_field, 
				array=array, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_array(self,array_field, array, collection_name, search_fields, approx=0, sum_fields=True, page_size=20, page=1, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/search_with_array',
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
				))

	@retry()
	@return_curl_or_response('json')
	def encode_dictionary_field(self,dictionary_fields, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/encode_dictionary_field',
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
			url='https://api.vctr.ai/collection/encode_dictionary',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				dictionary=dictionary, 
				dictionary_field=dictionary_field, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def search_with_dictionary(self, collection_name, search_fields, dictionary, dictionary_field, page_size=20, page=1, approx=0, sum_fields=True, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
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
dictionary: A dictionary to encode into vectors
dictionary_field: The dictionary field that encoding of the dictionary is trained on

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_dictionary',
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
				dictionary=dictionary, 
				dictionary_field=dictionary_field, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def encode_text(self,text, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/encode_text',
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
			url='https://api.vctr.ai/collection/bulk_encode_text',
			params=dict(
				texts=texts, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_text(self, collection_name, text, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
text: Text to encode into vector and vector search with
search_fields: Vector fields to search against

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_text',
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
				asc=asc, 
				text=text, 
				search_fields=search_fields, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def encode_image(self,image_url, model_url, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/encode_image',
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
			url='https://api.vctr.ai/collection/bulk_encode_image',
			params=dict(
				image_urls=image_urls, 
				model_url=model_url, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_image(self, collection_name, image_url, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
image_url: The image url of an image to encode into a vector
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_image',
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
				asc=asc, 
				image_url=image_url, 
				model_url=model_url, 
				search_fields=search_fields, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def search_with_image_upload(self, collection_name, image, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
image: Image represented as a base64 encoded string
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_image_upload',
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
				asc=asc, 
				image=image, 
				model_url=model_url, 
				search_fields=search_fields, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def encode_audio(self,audio_url, model_url, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/encode_audio',
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
			url='https://api.vctr.ai/collection/bulk_encode_audio',
			params=dict(
				audio_urls=audio_urls, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def search_with_audio(self, collection_name, audio_url, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
audio_url: The audio url of an audio to encode into a vector
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_audio',
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
				asc=asc, 
				audio_url=audio_url, 
				model_url=model_url, 
				search_fields=search_fields, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def search_with_audio_upload(self, collection_name, audio, model_url, search_fields, page=1, page_size=20, approx=0, sum_fields=True, metric="cosine", filters=[], facets=[], min_score=None, include_fields=[], include_vector=False, include_count=True, include_facets=False, hundred_scale=False, asc=False, **kwargs):
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
asc: Whether to sort results by ascending or descending order
audio: Audio represented as a base64 encoded string
model_url: The model url of a deployed vectorhub model
search_fields: Vector fields to search against

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_audio_upload',
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
				asc=asc, 
				audio=audio, 
				model_url=model_url, 
				search_fields=search_fields, 
				**kwargs))

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
			url='https://api.vctr.ai/collection/encode_fields_to_vector',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				vector_name=vector_name, 
				selected_fields=selected_fields, 
				**kwargs))

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
			url='https://api.vctr.ai/collection/encode_fields',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				vector_name=vector_name, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def search_with_fields(self, collection_name, search_fields, document, selected_fields, vector_name, page_size=20, page=1, approx=0, sum_fields=True, metric="cosine", min_score=None, include_fields=[], include_vector=False, include_count=True, hundred_scale=False, asc=False, **kwargs):
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
document: A document to encode into vectors
selected_fields: The fields to turn into vectors
vector_name: A name to call the vector that the fields turn into

"""
		return requests.post(
			url='https://api.vctr.ai/collection/search_with_fields',
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
				document=document, 
				selected_fields=selected_fields, 
				vector_name=vector_name, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def combine_vectors(self,vector_fields, vector_name, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/combine_vectors',
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
			url='https://api.vctr.ai/collection/collection_vector_mappings',
			params=dict(
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def insert_and_encode(self, collection_name, models, document={}, insert_date=True, overwrite=True, **kwargs):
		"""Insert a document into a Collection and encode it as well
When inserting the document you can specify your own id for a document by using the field name **"\_id"**. 
For specifying your own vector use the suffix (ends with)  **"\_vector\_"** for the field name.
e.g. "product\_description\_vector\_"
This method will also encode the specified field with models on the server side
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
document: A Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.
overwrite: Whether to overwrite document if it exists.
models: Field and model to encode it with. e.g.{'image_url':'image', 'audio_url':'audio', 'name':'text'}

"""
		return requests.post(
			url='https://api.vctr.ai/collection/insert_and_encode',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				document=document, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				models=models, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def bulk_insert_and_encode(self, collection_name, models, documents={}, insert_date=True, overwrite=True, **kwargs):
		"""Insert multiple documents into a Collection and encode it as well
When inserting the document you can specify your own id for a document by using the field name **"\_id"**. 
For specifying your own vector use the suffix (ends with)  **"\_vector\_"** for the field name.
e.g. "product\_description\_vector\_"
This method will also encode the specified field with models on the server side
    
Args
========
username: Username
api_key: Api Key, you can request it from request_api_key
collection_name: Name of Collection
documents: A list of documents. Document is a JSON-like data that we store our metadata and vectors with. For specifying id of the document use the field '\_id', for specifying vector field use the suffix of '\_vector\_'
insert_date: Whether to include insert date as a field 'insert_date_'.
overwrite: Whether to overwrite document if it exists.
models: Field and model to encode it with. e.g.{'image_url':'image', 'audio_url':'audio', 'name':'text'}

"""
		return requests.post(
			url='https://api.vctr.ai/collection/bulk_insert_and_encode',
			json=dict(
				username=self.username,
				api_key=self.api_key,
				collection_name=collection_name, 
				documents=documents, 
				insert_date=insert_date, 
				overwrite=overwrite, 
				models=models, 
				**kwargs))

	@retry()
	@return_curl_or_response('json')
	def job_status(self,job_id, job_name, collection_name, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/job_status',
			params=dict(
				job_id=job_id, 
				job_name=job_name, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def list_jobs(self,collection_name, show_active_only=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/list_jobs',
			params=dict(
				show_active_only=show_active_only, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def cluster(self,vector_field, collection_name, n_clusters=0, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/cluster',
			params=dict(
				vector_field=vector_field, 
				n_clusters=n_clusters, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def advanced_cluster(self,vector_field, collection_name, alias="default", n_clusters=0, n_iter=10, n_init=5, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/advanced_cluster',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				n_clusters=n_clusters, 
				n_iter=n_iter, 
				n_init=n_init, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def dimensionality_reduction(self,vector_field, collection_name, alias="default", n_components=0, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/dimensionality_reduction',
			params=dict(
				vector_field=vector_field, 
				alias=alias, 
				n_components=n_components, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_text_field(self,text_field, collection_name, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/encode_text_field',
			params=dict(
				text_field=text_field, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_audio_field(self,audio_field, collection_name, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/encode_audio_field',
			params=dict(
				audio_field=audio_field, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

	@retry()
	@return_curl_or_response('json')
	def encode_image_field(self,image_field, collection_name, refresh=True, **kwargs):
		return requests.get(
			url='https://api.vctr.ai/collection/jobs/encode_image_field',
			params=dict(
				image_field=image_field, 
				refresh=refresh, 
				username=self.username, 
				api_key=self.api_key, 
				collection_name=collection_name, 
				))

