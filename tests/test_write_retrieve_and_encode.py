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

@pytest.mark.use_client
def test_retrieve_and_encode_simple(test_client, test_collection_name):
    """Test retrieving documents and encoding them with vectors.
    """
    VECTOR_LENGTH = 100
    def fake_encode(x):
        return test_client.generate_vector(VECTOR_LENGTH)
    with TempClientWithDocs(test_client, test_collection_name, 100) as client:
        results = client.retrieve_and_encode(test_collection_name,
        models={'country': fake_encode})
        assert list(client.collection_schema(test_collection_name)['country_vector_'].keys())[0] == 'vector'
        assert len(results['failed_document_ids']) == 0
        assert 'country_vector_' in client.collection_schema(test_collection_name)
        docs = client.retrieve_documents(test_collection_name)['documents']
        assert len(docs[0]['country_vector_']) == VECTOR_LENGTH
