"""Smoke tests for the API - Ensure that these do not error out!
"""
import pytest 
import time
from ...utils import TempClientWithDocs

@pytest.mark.use_client
def test_smoke_compare_topk(test_analytics_client, document_vector_fields):
    with TempClientWithDocs(test_analytics_client) as client:
        time.sleep(2)
        results = test_analytics_client.random_compare_topk_documents_by_ids(
            collection_name=client.collection_name,
            vector_field=document_vector_fields[0]
        )

@pytest.mark.use_client
def test_smoke_compare_topk_vector(test_analytics_client, document_vector_fields):
    with TempClientWithDocs(test_analytics_client) as client:
        time.sleep(2)
        results = test_analytics_client.random_compare_topk_vectors(
            collection_name=client.collection_name,
            vector_fields=document_vector_fields
        )