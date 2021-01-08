"""Testing the various read functions for Vi
"""
import pytest
import time
from vectorai.errors import MissingFieldWarning, MissingFieldError
from .utils import TempClientWithDocs

class TestRead:
    @pytest.mark.use_client
    def test_setup_for_read(self, test_client, test_collection_name):
        """Test Setup for Read Operations"""
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        documents = test_client.create_sample_documents(5)
        test_client.insert_documents(
            collection_name=test_collection_name, documents=documents
        )
        time.sleep(10)
        assert True

    @pytest.mark.use_client
    def test_get_item_by_id(self, test_client, test_collection_name):
        return_item = test_client.id(collection_name=test_collection_name, document_id="0")
        for var in ['color', 'number', 'color_vector_', 'insert_date_']:
            assert var in return_item

    @pytest.mark.use_client
    def test_advanced_search_by_id(self, test_client, test_collection_name):
        filter_query = [
            {'field': 'color',
            'filter_type': 'text',
            'condition_value': 'red',
            'condition': '=='}
        ]
        results = test_client.advanced_search_by_id(test_collection_name, 
        document_id=test_client.random_documents(test_collection_name)['documents'][0]['_id'],
        fields={'color_vector_':1}, filters=filter_query)
        assert len(results) > 0

    @pytest.mark.use_client
    def test_get_document_by_bulk_id(self, test_client, test_collection_name):
        return_documents = test_client.bulk_id(
            collection_name=test_collection_name, document_ids=["0", "1"]
        )
        assert len(return_documents) == 2


    @pytest.mark.use_client
    def test_cleanup_for_read(self, test_client, test_collection_name):
        """Test Setup for Read Operations"""
        test_client.delete_collection(collection_name=test_collection_name)
        assert True

def test_get_field(test_client):
    """Test for accessing the document field.
    """
    test_dict = {"kfc": {"item": "chickens"}}
    assert test_client.get_field("kfc.item", doc=test_dict) == "chickens"

def test_get_empty_field(test_client):
    with pytest.raises(MissingFieldError):
        docs = test_client.create_sample_documents(10)
        test_client.get_field_across_documents('_id_', docs)

def test_check_schema(test_client):
    """Testing a nested dictionary to ensure it can detected a nested vector field
    """
    with pytest.warns(None) as record:
        nested_schema = {}
        test_client._check_schema(nested_schema)
        # nested_schema = {'chk': {'chk_vector_': [0, 2, 3]}}
    assert len(record) == 2
    assert test_client._check_schema(nested_schema) == (True, True)

def test_check_schema_with_vector_field(test_client):
    """Testing a nested dictionary to ensure it can detected a nested vector field
    """
    with pytest.warns(None) as record:
        nested_schema = {'chk': {'chk_vector_': [0, 2, 3]}}
        test_client._check_schema(nested_schema)
    assert len(record) == 1
    assert test_client._check_schema(nested_schema) == (True, False)

def test_check_schema_id_field(test_client):
    with pytest.warns(None) as record:
        nested_schema = {'_id': "text"}
        test_client._check_schema(nested_schema)
    assert len(record) == 1
    assert test_client._check_schema(nested_schema) == (False, True)

def test_check_schema_both(test_client):
    with pytest.warns(None) as record:
        nested_schema = {'_id': "text", "chk_vector_":[0, 1, 2]}
    assert len(record) == 0
    assert test_client._check_schema(nested_schema) == (False, False)

def test_search_collections(test_client):
    """
        Smoke test for searching collections
    """
    cn = 'example_collection_123y8io'
    test_client.create_collection(cn)
    assert len(test_client.search_collections('123y8io')) > 0, "Not searching collections properly."
    test_client.delete_collection(cn)

@pytest.mark.use_client
def test_random_recommendation_smoke_test(test_client, test_collection_name):
    """
        Smoke test for recommending random ID.
    """
    with TempClientWithDocs(test_client, test_collection_name):
        time.sleep(2)
        results = test_client.random_recommendation(
            test_collection_name, 
            field='color_vector_')
        assert len(results['results']) > 0, "Random recommendation fails."
