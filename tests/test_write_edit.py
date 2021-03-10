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

class TestEdit:
    @pytest.mark.use_client
    def test_setup_for_read(self, test_client, test_collection_name):
        """Test Setup for Read Operations"""
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(collection_name=test_collection_name)
        documents = [
            {
                "_id": "2",
                "document_vector_": test_client.generate_vector(vector_length=512),
                "attribute": "red",
            },
            {
                "_id": "1",
                "document_vector_": test_client.generate_vector(vector_length=512),
                "attribute": "blue",
            },
        ]

        test_client.insert_documents(
            collection_name=test_collection_name, documents=documents
        )
        time.sleep(10)
        assert True


    @pytest.mark.use_client
    def test_edit_document(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            edits = {
                "_id": "1",
                "location": "Paris"
            }
            client.edit_document(
                collection_name=test_collection_name, edits=edits, document_id=edits['_id']
            )
            time.sleep(2)
            doc = client.id(collection_name=test_collection_name, document_id="1")
            assert doc["location"] == "Paris"

    @pytest.mark.use_client
    def test_create_filter(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            doc = {
                'location': "Paris"
            }
            client.insert(test_collection_name, doc)
            results = test_client.filters(
                test_collection_name,
                test_client.create_filter_query(test_collection_name, 'location', 'contains', 'Paris'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_create_filter_2(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            doc = {
                'location': "Paris"
            }
            client.insert(test_collection_name, doc)
            results = test_client.filters(
                test_collection_name,
                test_client.create_filter_query(
                    test_collection_name, 'location', 'exact_match', 'Paris'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_create_filter_3(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            results = test_client.filters(test_collection_name,
            test_client.create_filter_query(test_collection_name, 'size.feet', '<=', '31'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_create_filter_4(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name):
            results = test_client.filters(test_collection_name,
            test_client.create_filter_query(test_collection_name, 'insert_date_', '>=', '2020-01-01'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_edit_documents(self, test_client, test_collection_name):
        """Test adding of an attribute
        """
        with TempClientWithDocs(test_client, test_collection_name):
            edits = [
                {"_id": "2", "location": "Sydney",},
                {"_id": "1", "location": "New York",},
            ]
            test_client.edit_documents(test_collection_name, edits)
            doc = test_client.id(collection_name=test_collection_name, document_id="2")
            assert doc["location"] == "Sydney"
            doc = test_client.id(collection_name=test_collection_name, document_id="1")
            assert doc['location'] == 'New York'

@pytest.mark.use_client
def test_edit_documents(test_client, test_collection_name):
    with TempClientWithDocs(test_client, test_collection_name, 100) as client:
        edits = test_client.create_sample_documents(100)
        {x.update({'favorite_singer': 'billie eilish'}) for x in edits}
        response = client.edit_documents(test_collection_name, edits)
        assert response['edited_successfully'] == len(edits)
        # Retrieve the documents 
        docs = client.retrieve_documents(test_collection_name, 
        include_fields=['favorite_singer'], page_size=1)['documents']
        for doc in docs:
            assert doc['favorite_singer'] == 'billie eilish' 
