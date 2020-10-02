"""Test the write database.
"""
import json
import pytest
import os
import time
import numpy as np
try:
    import tensorflow as tf
    from vectorai.models.transformer_models import Transformer2Vec
except:
    pass
from vectorai.write import ViWriteClient
from vectorai.errors import APIError
from vectorai.client import ViClient


class TestCollectionBasics:
    @pytest.mark.use_client
    def test_create_collection(self, test_client, test_collection_name, test_vector_field):
        collection_name = test_collection_name
        if collection_name in test_client.list_collections():
            test_client.delete_collection(collection_name)
        response = test_client.create_collection(
            collection_name=collection_name, collection_schema={test_vector_field: 512}
        )
        assert response is None

    @pytest.mark.use_client
    def test_prevent_collection_overwrite(self, test_client, test_collection_name):
        """
            Test prevention of the overwriting of the collections.
        """
        if test_collection_name not in test_client.list_collections():
            test_client.create_collection(test_collection_name)
        with pytest.raises(APIError):
            response = test_client.create_collection(collection_name=test_collection_name)

    @pytest.mark.use_client
    def test_list_collections(self, test_collection_name, test_client):
        response = test_client.list_collections()
        assert response.count(test_collection_name) == 1

    @pytest.mark.use_client
    def test_delete_collection(self, test_client, test_collection_name):
        response = test_client.delete_collection(collection_name=test_collection_name)
        assert response['status'] == 'complete'


def test__as_json(test_client):
    sample_document = {
        "val": np.rand(20), 
        "val_2": np.rand(100)
    }
    sample_document_result = test_client._as_json(sample_document)
    assert sample_document_result == sample_document


def assert_json_serializable(document, temp_json_file="test.json"):
    """Assert that an document is json serializable and is the same after loading back into Python.
    """
    with open(temp_json_file, "w") as f:
        json.dump(document, f)
    return_document = json.load(open(temp_json_file, "r"))
    os.remove(temp_json_file)
    assert return_document == document


def test__as_json(test_client):
    """Test automatic JSON conversion for numpy arrays.
    """
    sample_document = {"val": np.random.rand(20), "val_2": np.random.rand(100)}
    sample_document_result = test_client._as_json(sample_document)
    assert_json_serializable(sample_document_result)

@pytest.mark.use_tensorflow
def test__as_json_tensorflow(test_client):
    """Test automatic JSON conversion for tensorflow tensors.
    """
    sample_document = {
        "val": tf.random.uniform((1, 20)),
        "val_2": tf.random.uniform((1, 20)),
    }
    sample_document_result = test_client._as_json(sample_document, flatten=True)
    assert_json_serializable(sample_document_result)

@pytest.mark.use_tensorflow
def test__as_json_tensorflow_error_raise(test_client):
    """Test that error is raised with tensorflow conversion when rank (ndims) is greater than 2.
    """
    sample_document = {"val": tf.random.uniform((1, 1, 20))}
    with pytest.raises(APIError):
        sample_document_result = test_client._as_json(sample_document)


class TestInsert:   
    @pytest.mark.use_client
    def test_insert_single_document(self, test_client, test_collection_name):
        if test_collection_name not in test_client.list_collections():
            test_client.create_collection(test_collection_name)
        document = {"sample_vector_": test_client.generate_vector(20), "sample_name": "hi"}
        response = test_client.insert_document(
            collection_name=test_collection_name, document=document
        )
        assert response is None

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
            response = test_client.insert_document(
                collection_name=test_collection_name, document=document
            )


    @pytest.mark.use_client
    def test_clean_up(self, test_client, test_collection_name):
        """Remove a collection if it is there.
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        assert test_collection_name not in test_client.list_collections()


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
        assert True


    @pytest.mark.use_client
    def test_edit_document(self, test_client, test_collection_name):
        test_client.insert_documents(test_collection_name, 
        test_client.create_sample_documents(10))
        edits = {
            "_id": "1",
            "location": "Paris"
        }
        test_client.edit_document(
            collection_name=test_collection_name, edits=edits
        )
        time.sleep(5)
        doc = test_client.id(test_collection_name, document_id="1")
        assert doc["location"] == "Paris"

    @pytest.mark.use_client
    def test_edit_documents(self, test_client, test_collection_name):
        """Test adding of an attribute
        """
        edits = [
            {"_id": "2", "location": "Sydney",},
            {"_id": "1", "location": "New York",},
        ]
        test_client.edit_documents(test_collection_name, edits, workers=2)
        doc = test_client.id(test_collection_name, document_id="2")
        assert doc["location"] == "Sydney"
        doc = test_client.id(test_collection_name, document_id="1")
        assert doc['location'] == 'New York'
    
    @pytest.mark.use_client
    def test_cleanup(self, test_client, test_collection_name):
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)


# @pytest.mark.skip("Embed function is on pause until there is more clarity.")
# def test_multiple_insert_documents_embed(
#     test_client,
#     test_api_key,
#     test_username,
#     test_collection_name,
#     test_vector_field,
#     test_id_field,
# ):
#     documents = [
#         {"_id": "5", "attribute": "violet"},
#         {"_id": "6", "attribute": "black"},
#     ]

#     class Model:
#         def encode(self, document):
#             return test_client.generate_vector(512)

#     model = Model()

#     test_client.insert_documents(
#         test_collection_name, documents=documents, models={test_vector_field: model}
#     )

#     return_document = test_client.id(
#         collection_name=test_collection_name, document_id="5"
#     )
#     assert return_document["attribute"] == "violet"
#     return_document = test_client.id(
#         collection_name=test_collection_name, document_id="6"
#     )
#     assert return_document["attribute"] == "black"


# @pytest.mark.skip(
#     "Function embedding needs to be more " + "thoroughly discussed and may change."
# )
# def test_insert_document_embed(
#     test_client, test_api_key, test_username, test_collection_name
# ):
#     # The embed function string most be reproducible
#     # test_client = ViClient(username="test")
#     embed_func_str = f"""from vectorai import ViClient
# test_client = ViClient("{test_username}", "{test_api_key}")
# def embed_function(document):
#     return test_client.generate_vector(512)
# """
#     document = {"_id": 2, "attribute": "orange"}
#     test_client.insert_document(
#         collection_name=test_collection_name,
#         document=document,
#         use_embed_func=True,
#         embed_func_list=[embed_func_str],
#         search_vector_fields=["document_vector_"],
#     )

def test__write_document_nested_field():
    sample = {"this": {}}
    ViWriteClient.set_field("this.is", doc=sample, value=[0, 2])
    assert sample["this"]["is"] == [0, 2]

def test__write_document_nested_field_2():
    sample = {"this": {"is": {}}}
    ViWriteClient.set_field("this.is", doc=sample, value=[0, 2])
    assert sample["this"]["is"] == [0, 2]

@pytest.mark.use_tensorflow
def test__encode_documents_with_models(test_client, sample_documents):
    """Test Model Encoding
    """
    model = Transformer2Vec('distilbert')
    roberta_model = Transformer2Vec('distilroberta')
    test_client._encode_documents_with_models(sample_documents, models={'team': [model, roberta_model]})
    assert 'distilbert' in test_client.get_name(model)
    assert 'roberta' in test_client.get_name(roberta_model)
    assert 'team_distilroberta_text_vector_' in sample_documents[0].keys()
    assert 'team_distilbert_text_vector_' in sample_documents[0].keys()

@pytest.mark.use_client
def test_encode_documents_with_deployed_model(test_client, test_text_encoder):
    """
        Test single encoding method for models.
    """
    documents = test_client.create_sample_documents(10)
    test_client._encode_documents_with_models(documents, models={'color': [test_text_encoder]}, use_bulk_encode=False)
    assert 'color_vector_' in documents[0].keys()
    assert len(documents[0]['color_vector_']) > 0

@pytest.mark.use_client
def test_bulk_encode_documents_with_deployed_model(test_client, test_text_encoder):
    """
        Test bulk encoding method for models.
    """
    # Test when model key input is a list
    documents = test_client.create_sample_documents(10)
    test_client._encode_documents_with_models_in_bulk(documents, models={'color': [test_text_encoder]}, use_bulk_encode=True)
    assert 'color_vector_' in documents[0].keys()
    assert len(documents[0]['color_vector_']) > 0
    del documents
    documents = test_client.create_sample_documents(10)
    test_client._encode_documents_with_models_in_bulk(documents, models={'color': test_text_encoder}, use_bulk_encode=True)
    assert 'color_vector_' in documents[0].keys()
    assert len(documents[0]['color_vector_']) > 0

@pytest.mark.use_client
def test_multiprocess_insert(test_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 10
    if test_collection_name in test_client.list_collections():    
        test_client.delete_collection(test_collection_name)
    documents = test_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    results = test_client.insert_documents(test_collection_name, documents, workers=5)
    assert len(results['failed_document_ids']) == 0
    assert test_collection_name in test_client.list_collections()
    assert test_client.collection_stats(test_collection_name)['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_insert_with_error(test_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 10
    if test_collection_name in test_client.list_collections():    
        test_client.delete_collection(test_collection_name)
    documents = test_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    documents.append({
        '_id': 3,
        'color': np.nan
    })
    
    # This should result in 1 failure
    results = test_client.insert_documents(test_collection_name, documents, workers=5)
    assert len(results['failed_document_ids']) == 1
    assert test_collection_name in test_client.list_collections()
    assert test_client.collection_stats(test_collection_name)['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_with_collection_client(test_collection_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 10
    if test_collection_client.collection_name in test_collection_client.list_collections():    
        test_collection_client.delete_collection()
    documents = test_collection_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    results = test_collection_client.insert_documents(documents, workers=5)
    assert len(results['failed_document_ids']) == 0
    assert test_collection_client.collection_name in test_collection_client.list_collections()
    assert test_collection_client.collection_stats()['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_collection_client.delete_collection()

@pytest.mark.use_client
def test_multiprocess__with_error_with_collection_client(test_collection_client):
    NUM_OF_DOCUMENTS_INSERTED = 10
    if test_collection_client.collection_name in test_collection_client.list_collections():    
        test_collection_client.delete_collection()
    documents = test_collection_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    documents.append({
        '_id': 3,
        'color': np.nan
    })
    # This should result in 1 failure
    results = test_collection_client.insert_documents(documents, workers=5)
    assert len(results['failed_document_ids']) == 1
    assert test_collection_client.collection_name in test_collection_client.list_collections()
    assert test_collection_client.collection_stats()['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_collection_client.delete_collection()
