"""
Write Operations for Vi that involves inserting documents, editing or deleting documents.
"""
import io
import gc
import types
import json
import base64
import warnings
import requests
import pandas as pd
import numpy as np
import copy
from tqdm.notebook import tqdm
from typing import List, Dict, Union, Any, Callable
from functools import partial
from multiprocessing import Pool
from .utils import UtilsMixin
from .errors import APIError
from .read import ViReadClient
from .api.write import ViWriteAPIClient


class ViWriteClient(ViReadClient, ViWriteAPIClient, UtilsMixin):
    """Class to write to database."""

    def __init__(self, username, api_key, url="https://api.vctr.ai" ):
        self.username = username
        self.api_key = api_key
        self.url = url

    @staticmethod
    def _raise_error(response):
        """
        Internal Error check if there is a 'status' key.

        Args:
            response:
                A python dictionary/JSON response that contains the response function

        Example:

            >>> from vectorai.client import ViClient
            >>> response = requests.get(...) 
            >>> ViClient._raise_error(response)
        """
        if 'status' in response.keys():
            if response["status"].lower() == "error":
                raise APIError(response["message"])

    @classmethod
    def _chunks(self, lst: List, n: int):
        """
        Chunk an iterable object in Python but not a pandas DataFrame.

        Args:
            lst:
                Python List
            n:
                The chunk size of an object.

        Example:
            >>> documents = [{...}]
            >>> ViClient.chunk(documents)
        """
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    @staticmethod
    def chunk(documents: Union[pd.DataFrame, List], chunk_size: int = 20):
        """
        Chunk an iterable object in Python.

        Args:
            documents:
                List of dictionaries/Pandas dataframe
            chunk_size:
                The chunk size of an object.

        Example:
            >>> documents = [{...}]
            >>> ViClient.chunk(documents)
        """
        if isinstance(documents, pd.DataFrame):
            for i in range(0, len(documents), chunk_size):
                yield documents.iloc[i : i + chunk_size]
        else:
            for i in range(0, len(documents), chunk_size):
                yield documents[i : i + chunk_size]

    @staticmethod
    def dummy_vector(vector_length):
        """
        Dummy vector for missing vector fields.

        Args:
            collection_name:
                Name of collection

            edits:
                What edits to make in a collection.
            
            document_id:
                Id of the document 

        Example:
            >>> from vectorai.client import ViClient
            >>> dummy_vector = ViClient.dummy_vector(20)
        """
        return [1e-7] * vector_length

    @staticmethod
    def set_field(
        field: str, doc: Dict, value: Any, handle_if_missing=True
    ):
        """
        For nested dictionaries, tries to write to the respective field.
        If you toggle off handle_if_misisng, then it will output errors if the field is 
        not found.
        e.g.
        field = kfc.item
        value = "fried wings"
        This should then create the following entries if they dont exist:
        {
            "kfc": {
                "item": "fried wings"
            }
        }

        Args:
            field:
                Field of the document to write.
            doc: 
                Python dictionary
            value:
                Value to write

        Example:

            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> sample_document = {'kfc': {'item': ''}}
            >>> vi_client.set_field('kfc.item', sample_document, 'chickens')
        """
        fields = field.split(".")
        # Assign a pointer.
        d = doc
        for i, f in enumerate(fields):
            # Assign the value if this is the last entry e.g. stores.fastfood.kfc.item will be item
            if i == len(fields) - 1:
                d[f] = value
            else:
                if f in d.keys():
                    d = d[f]
                else:
                    d.update({f: {}})
                    d = d[f]

    def create_collection(self, collection_name: str, collection_schema: Dict = {}):
        """
        Create a collection

        A collection can store documents to be searched, retrieved, filtered and aggregated (similar to Collections in MongoDB, Tables in SQL, Indexes in ElasticSearch).

        If you are inserting your own vector use the suffix (ends with) "_vector_" for the field name. and specify the length of the vector in colletion_schema like below example::

            {
                "collection_schema": {
                    "celebrity_image_vector_": 1024,
                    "celebrity_audio_vector" : 512,
                    "product_description_vector" : 128
                }
            }

        Args:
            collection_name:
                Name of a collection
            collection_schema:
                A collection schema. This is necessary if the first document is not representative of the overall schema collection. This should be specified if the items need to be edited. The schema needs to look like this : { vector_field_name: vector_length }

        Example:
            >>> collection_schema = {'image_vector_':2048}
            >>> ViClient.create_collection(collection_name, collection_schema)
        """
        response = self._create_collection(
            collection_name, collection_schema=collection_schema
        )
        self._raise_error(response)
        print(f"Collection {collection_name} created successfully.")

    def delete_collection(self, collection_name: str):
        """
        Delete the collection via the colleciton name.

        Args:
            collection_name:
                Name of collection to delete.

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.delete_collection(collection_name)
        """
        return self._delete_collection(collection_name)

    def _get_vector_name_for_encoding(self, f: str, model: Callable, model_list: List[Callable]):
        """
        Returns the vector names for encoding.
        
        Args:
            f:
                Field to encode
            model:
                The model used for encoding
            models:
                A dictionary of fields and models to determine the type of encoding for each field.

        """
        if len(model_list) == 1 and self.get_name(model) is None:
            vector_name = f"{f}_vector_"
        elif isinstance(model, (types.FunctionType, types.MethodType)):
            vector_name = f"{f}_vector_"
        else:
            vector_name = f"{f}_{self.get_name(model)}_vector_"
        return vector_name

    def _check_if_multiple_models_have_same_name(self, models: Dict):
        """
            For a model dictionary, ensure that the name of a function is good.

            Args:
                models:
                    A dictionary where a key links to a dictionary.

        """
        for f, model_list in models.items():
            if not isinstance(model_list, list):
                model_list = [model_list]
            name_list = []
            for model in model_list:
                name = self.get_name(model)
                if name is None and len(model_list) > 1:
                    assert self.get_name(m) is not None, f"Your models are missing names. Please set name using set_name(model) function."
                name_list.append(name)
            if len(set(name_list)) != len(name_list):
                raise ValueError("Models have the set name. Check each model name is unique.")

    def encode_documents_with_models_using_encode(self, documents: List[Dict], models: Dict):
        """
        Encode documents with appropriate models without a bulk_encode function.
        Args:
            documents: 
                List of documents/JSONs/dictionaries. 
            models:
                A dictionary of fields and models to determine the type of encoding for each field. 
        
        """
        for d in documents:
            for f, model_list in models.items():
                # Typecast callable to a list to easily pass through for-loop.
                if not isinstance(model_list, list):
                    model_list = [model_list]
                for model in model_list:
                    vector_field = self._get_vector_name_for_encoding(f, model, model_list)
                    if not self.is_field(f, d):
                        warnings.warn(f"""Missing {f} in a document. We will fill the missing with empty vectors.""")
                        try:
                            self.set_field(vector_field, d, self.dummy_vector(vector_length))
                        except:
                            raise APIError("Need to ensure at least one passthrough is made to get vector length.")
                    if isinstance(model, (types.FunctionType, types.MethodType)):
                        vector = model(self.get_field(f, d))
                        vector_length = len(vector)
                        self.set_field(vector_field, d, vector)
                    else:
                        if not hasattr(model, "encode"):
                            raise APIError("Not sure how to encode. Please sure the model class has an encode method.")
                        self.set_field(vector_field, d, model.encode(self.get_field(f, d)))
        return documents
    
    def encode_documents_with_models(
        self, documents: List[Dict], models: Union[Dict[str, Callable], List[Dict]] = {}, use_bulk_encode=False
    ):
        """
        Encode documents with appropriate models.
        
        Args:
            documents:
                List of documents/jsons/dictionaries.
            models:
                A dictionary of fields and models to determine the type of encoding for each field.
        
        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> from vectorai.models.deployed import ViText2Vec
            >>> text_encoder = ViText2Vec(username, api_key, vectorai_url)
            >>> documents = [{'chicken': 'Big chicken'}, {'chicken': 'small_chicken'}, {'chicken': 'cow'}]
            >>> vi_client.encode_documents_with_models(documents=documents, models={'chicken': text_encoder.encode})
        """
        # TODO: refactor & test if changing black length
        self._check_if_multiple_models_have_same_name(models)
        if use_bulk_encode:
            return self.encode_documents_with_models_in_bulk(documents=documents, models=models)
        else:
            return self.encode_documents_with_models_using_encode(documents=documents, models=models)
                                
    def encode_documents_with_models_in_bulk(self, documents: List[Dict], models: Dict):
        """
        Encode documents with models to allow for bulk_encode.
        
        Args:
            documents:
                List of documents/jsons/dictionaries.
            models:
                A dictionary of fields and models to determine the type of encoding for each field.
        """
        # Ensure all models have a bulk_encode method.
        for f, model_list in models.items():
            if not isinstance(model_list, list):
                models[f] = [model_list]
            for model in models[f]:
                if model.__name__ is not None:
                    assert hasattr(model, 'bulk_encode'), f"Model {model.__name__} cannot be encoded in bulk. Missing bulk_encode method."    
                else:
                    assert hasattr(model, 'bulk_encode'), "Model cannot be encoded in bulk. Missing bulk_encode method."
        # Now bulk-encode and then set the field for each dictionary
        for f, model_list in models.items():
            for model in model_list:
                vector_field = self._get_vector_name_for_encoding(f, model, model_list)
                values = self.get_field_across_documents(f, documents)
                vectors = model.bulk_encode(values)
                self.set_field_across_documents(vector_field, vectors, documents)
        return documents

    def _insert_and_encode(
        self, documents: list, collection_name: str, models: dict, verbose=False, 
        use_bulk_encode=False, overwrite=False, missing_ids=None
    ):
        """
            Insert and encode documents
        """
        if not overwrite:
            documents = [doc for i, doc in enumerate(documents) if self.get_field('_id', doc) in missing_ids]
        
        if len(documents) == 0:
            return {
                'failed_document_ids': []
            }
        return self.bulk_insert(
            collection_name=collection_name,
            documents=self.encode_documents_with_models(documents, models=models, 
            use_bulk_encode=use_bulk_encode), 
            overwrite=overwrite
        )
        
    def insert_document(self, collection_name: str, document: Dict, verbose=False):
        """
        Insert a document into a collection

        Args:
            collection_name: 
                Name of collection
            
            documents:
                List of documents/jsons/dictionaries.

        Example:
            >>> from vectorai.models.deployed import ViText2Vec
            >>> text_encoder = ViText2Vec(username, api_key, vectorai_url)
            >>> document = {'chicken': 'Big chicken'}
            >>> vi_client.insert_document(document)
        """
        response = self.insert(collection_name=collection_name, document=document)
        if response != "inserted":
            raise APIError(f"Document failed to insert into {collection_name}")
        
        if verbose:
            print(f"Document inserted succesfully into {collection_name}")
            

    def insert_single_document(self, collection_name: str, document: Dict):
        """
        Encode documents with models.
        

        Args:
            documents:
                List of documents/jsons/dictionaries.

        Example:
            >>> from vectorai.models.deployed import ViText2Vec
            >>> text_encoder = ViText2Vec(username, api_key, vectorai_url)
            >>> document = {'chicken': 'Big chicken'}
            >>> vi_client.insert_single_document(document)
        """
        return self.insert_document(collection_name=collection_name, document=document)

    def insert_documents(
        self,
        collection_name: str,
        documents: List,
        models: Dict[str, Callable] = {},
        chunksize: int = 15,
        workers: int = 1,
        verbose: bool=False,
        use_bulk_encode: bool=False,
        overwrite: bool=False,
        show_progress_bar: bool=True
    ):
        """
        Insert documents into a collection with an option to encode with models.        

        Args:
            collection_name:
                Name of collection
            documents:
                All documents.
            models:
                Models with an encode method 
            use_bulk_encode:
                Use the bulk_encode method in models
            verbose:
                Whether to print document ids that have failed when inserting.
            overwrite:
                If True, overwrites document based on _id field.

        Example:
            >>> from vectorai.models.deployed import ViText2Vec
            >>> text_encoder = ViText2Vec(username, api_key, vectorai_url)
            >>> documents = [{'chicken': 'Big chicken'}, {'chicken': 'small_chicken'}, {'chicken': 'cow'}]
            >>> vi_client.insert_documents(documents, models={'chicken': text_encoder.encode})
        """
        if collection_name not in self.list_collections():
            if len(models) == 0:
                self._check_schema(documents[0])
            self.create_collection_from_document(
                collection_name,
                self.encode_documents_with_models([documents[0]], models)[0],
            )
        failed = []
        bulk_id_list = self.get_field_across_documents('_id', documents)
        missing_ids = set(self.bulk_missing_id(collection_name, bulk_id_list))
        iter_len = int(len(documents) / chunksize) + (len(documents) % chunksize > 0)
        iter_docs = self._chunks(documents, chunksize)

        if workers == 1:
            for c in self.progress_bar(iter_docs, total=iter_len, show_progress_bar=show_progress_bar):
                result = self._insert_and_encode(
                    documents=c, collection_name=collection_name, models=models, use_bulk_encode=use_bulk_encode,
                    missing_ids=missing_ids, overwrite=overwrite
                )
                self._raise_error(result)
                if verbose: print(f"Failed: {result['failed_document_ids']}")
                failed.append(result["failed_document_ids"])
        else:
            pool = Pool(processes=workers)
            # Using partial insert for compatibility with ViCollectionClient
            partial_insert = partial(self._insert_and_encode, models=models,collection_name=collection_name,
            missing_ids=missing_ids, overwrite=overwrite)
            for result in self.progress_bar(
                pool.imap_unordered(func=partial_insert, iterable=iter_docs), total=iter_len):
                self._raise_error(result)
                if verbose and len(result['failed_document_ids']) > 0:
                    warnings.warn("""There are failed documents. Try re-inserting these IDs
                    and test by choosing the most important fields first!""")
                    print(f"Failed: {result['failed_document_ids']}")
                failed.append(result["failed_document_ids"])
            pool.close()
            pool.join()
        failed = self.flatten_list(failed)
        return {
            "inserted_successfully": len(documents) - len(failed),
            "failed": len(failed),
            "failed_document_ids": failed,
        }


    def insert_df(
        self,
        collection_name: str,
        df: pd.DataFrame,
        models: Dict[str, Callable] = {},
        chunksize: int = 15,
        workers: int = 1,
        verbose: bool = True,
        use_bulk_encode: bool = False,
    ):
        """
        Insert dataframe into a collection
        
        Args:
            collection_name:
                Name of collection
            df:
                Pandas DataFrame
            models:
                Models with an encode method
            verbose:
                Whether to print document ids that have failed when inserting.

        Example:
            >>> from vectorai.models.deployed import ViText2Vec
            >>> text_encoder = ViText2Vec(username, api_key, vectorai_url)
            >>> documents_df = pd.DataFrame.from_records([{'chicken': 'Big chicken'}, {'chicken': 'small_chicken'}, {'chicken': 'cow'}])
            >>> vi_client.insert_df(documents=documents_df, models={'chicken': text_encoder.encode})
        """
        return self.insert_documents(
            collection_name,
            json.loads(df.to_json(orient="records")),
            models=models,
            chunksize=chunksize,
            workers=workers,
            verbose=verbose,
            use_bulk_encode=use_bulk_encode
        )

    def edit_document(self, collection_name: str, edits: Dict[str, str], verbose=True):
        """
        Edit a document ina collection based on ID
        

        Args:
            collection_name:
                Name of collection

            edits:
                What edits to make in a collection.
            
            document_id:
                Id of the document 

        Example:            Example:
                >>> from vectorai.client import ViClient
                >>> vi_client = ViClient(username, api_key, vectorai_url)
                >>> vi_client.edit_documents(collection_name, edits=documents, workers=10)
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> documents_df = pd.DataFrame.from_records([{'chicken': 'Big chicken'}, {'chicken': 'small_chicken'}, {'chicken': 'cow'}])
            >>> vi_client.edit_document(documents=documents_df, models={'chicken': text_encoder.encode})
        """
        if "_id" not in edits.keys():
            raise ValueError("Missing _id in the document. Please include that field.")
        copy_doc = edits.copy()
        copy_doc.pop('_id')
        document_id = edits['_id']
        response = self._edit_document(
            collection_name, edits=copy_doc, document_id=document_id
        )

        VERBOSE_MESSAGE_DICT = {
            'updated': f"Edited item with id {document_id} successfully.",
            'no changes detected': f"{document_id} has no changes."
        }

        if response not in VERBOSE_MESSAGE_DICT.keys():
            raise APIError("Failed to edit item.")
        
        if verbose:
            print(VERBOSE_MESSAGE_DICT[response])
            

    def _edit_document_return_id(
        self, edits: Dict[str, str], collection_name: str
    ):
        """
            Edit documents when ID is returned.
        

            Args:
                collection_name:
                    Name of collection

                edits:
                    What edits to make in a collection. Ensure that _id is stored in the document.

        """
        copy_doc = edits.copy()
        if '_id' not in edits.keys():
            warnings.warn("One of the documents is missing an _id field.")
        copy_doc.pop('_id')
        response = self._edit_document(
            collection_name=collection_name, edits=copy_doc, document_id=edits["_id"]
        )
        if response == "failed":
            return edits["_id"]
        return

    def edit_documents(self, collection_name: str, edits: Dict, workers: int = 1):
        """
            Edit documents in a collection
        

            Args:
                collection_name:
                    Name of collection

                edits:
                    What edits to make in a collection. Ensure that _id is stored in the document.
                
                workers:
                    Number of parallel processes to run.

            Example:
                >>> from vectorai.client import ViClient
                >>> vi_client = ViClient(username, api_key, vectorai_url)
                >>> vi_client.edit_documents(collection_name, edits=documents, workers=10)
        """
        failed = []
        if workers == 1:
            for c in self.progress_bar(edits):
                result = self._edit_document_return_id(collection_name=collection_name, edits=c)
                if result is not None:
                    failed.append([result])
        else:
            pool = Pool(processes=workers)
            for result in self.progress_bar(
                pool.imap_unordered(
                    func=partial(self._edit_document_return_id, collection_name=collection_name),
                    iterable=edits
                ),
                total=int(len(edits) / workers)
            ):
                if result is not None:
                    failed.append([result])
            pool.close()
            pool.join()
        failed = self.flatten_list(failed)
        return {
            "edited_successfully": len(edits) - len(failed),
            "failed": len(failed),
            "failed_document_ids": failed,
        }
