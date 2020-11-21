"""
    Testing for search functions
"""
import numpy as np
import pytest
import time

@pytest.mark.use_client
def test_chunk_search(test_client, test_collection_name):
    test_client.insert_documents(test_collection_name, 
    test_client.create_sample_documents(10, include_chunks=True))
    time.sleep(5)
    results = test_client.chunk_search(test_collection_name,
    vector=np.random.rand(1, 30).tolist()[0],
    search_fields=['chunk.color_chunkvector_'])
    assert 'error' not in results.keys()
