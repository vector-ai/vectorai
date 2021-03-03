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
def test_encode_documents_with_deployed_model(test_client, test_text_encoder):
    """
        Test single encoding method for models.
    """
    documents = test_client.create_sample_documents(10)
    test_client.encode_documents_with_models(documents, models={'color': [test_text_encoder]}, use_bulk_encode=False)
    assert 'color_vector_' in documents[0].keys()
    assert len(documents[0]['color_vector_']) > 0

@pytest.mark.use_client
def test_bulk_encode_documents_with_deployed_model(test_client, test_text_encoder):
    """
        Test bulk encoding method for models.
    """
    # Test when model key input is a list
    documents = test_client.create_sample_documents(10)
    test_client.encode_documents_with_models(documents, models={'color': [test_text_encoder]}, use_bulk_encode=True)
    assert 'color_vector_' in documents[0].keys()
    assert len(documents[0]['color_vector_']) > 0
    del documents
    documents = test_client.create_sample_documents(10)
    test_client.encode_documents_with_models(documents, models={'color': test_text_encoder}, use_bulk_encode=True)
    assert 'color_vector_' in documents[0].keys()
    assert len(documents[0]['color_vector_']) > 0
