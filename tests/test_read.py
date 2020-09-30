"""Testing the various read functions for Vi
"""
import pytest

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
        assert True

    @pytest.mark.use_client
    def test_get_item_by_id(self, test_client, test_collection_name):
        return_item = test_client.id(collection_name=test_collection_name, document_id="0")
        for var in ['color', 'number', 'color_vector_', 'insert_date_']:
            assert var in return_item

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

def test_read(test_client):
    """Testing a nested dictionary to ensure it can detected a nested vector field
    """
    nested_schema = {'chk': {'chk_vector_': [0]}}
    assert test_client._check_schema(nested_schema) is False
