"""Test the write database.
"""
import json
import pytest
import os
import time
import numpy as np
from vectorai.models.deployed import ViText2Vec
from vectorai.write import ViWriteClient
from vectorai.errors import APIError, MissingFieldError, MissingFieldWarning, CollectionNameError
from vectorai.client import ViClient
from .utils import TempClientWithDocs

class TestInsert:
    @pytest.mark.use_client
    def test_insert_documents_simple_and_collection_stats_match(self, test_client, 
    test_collection_name):
        """
            Testing for simple document insertion
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        test_client.insert_documents(test_collection_name, sample_documents)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_without_id_fields(self, test_client, test_collection_name):
        """
            Test inserting documents if they do not have an ID field.
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Remove the ID fields
        {x.pop('_id') for x in sample_documents}
        test_client.insert_documents(test_collection_name, sample_documents)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_without_id_fields_with_overwrite(self, test_client, 
    test_collection_name):
        """
            Test inserting documents if they do not have an ID field.
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Remove the ID fields
        {x.pop('_id') for x in sample_documents}
        with pytest.warns(MissingFieldWarning):
            test_client.insert_documents(test_collection_name, sample_documents, overwrite=True)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_when_id_is_not_a_string(self, test_client, test_collection_name):
        """
            Test inserting documents when ID is not a string
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Create integer IDs strings
        {x.update({'_id': int(x['_id'])}) for x in sample_documents}
        test_client.insert_documents(test_collection_name, sample_documents, overwrite=False)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_when_id_is_not_a_string_with_overwrite(self, test_client, 
    test_collection_name):
        """
            Test inserting documents when ID is not a string
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Create integer IDs strings
        {x.update({'_id': int(x['_id'])}) for x in sample_documents}
        test_client.insert_documents(test_collection_name, sample_documents, overwrite=True)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_insert_single_document(self, test_client, test_collection_name):
        if test_collection_name not in test_client.list_collections():
            test_client.create_collection(test_collection_name)
        # document = {"sample_vector_": test_client.generate_vector(20), "sample_name": "hi"}
        document = test_client.create_sample_document(1)
        response = test_client.insert(
            collection_name=test_collection_name, document=document
        )
        assert response['status'] == 'successful'

    @pytest.mark.use_client
    def test_insert_single_document_error(self, test_client, test_collection_name):
        """Trigger an insert fail error
        """
        with pytest.raises(APIError):
            if test_collection_name not in test_client.list_collections():
                test_client.create_collection(test_collection_name)
            document = {
                "sample_vectors_": [test_client.generate_vector(20)] + [np.nan],
                "samplename": [["hi"]],
            }
            response = test_client.insert(
                collection_name=test_collection_name, document=document
            )


    @pytest.mark.use_client
    def test_clean_up(self, test_client, test_collection_name):
        """Remove a collection if it is there.
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        assert test_collection_name not in test_client.list_collections()
