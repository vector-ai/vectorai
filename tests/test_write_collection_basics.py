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

def test_dummy_vector(test_client):
    """
        Test the dummy vector
    """
    assert len(test_client.dummy_vector(512)) == 512

def test_set_field_on_new_field(test_client):
    """
        Assert when set on new field.
    """
    doc = {}
    test_client.set_field('balls', doc, 3)
    assert doc['balls'] == 3

def test_set_field_on_new_dict(test_client):
    doc = {}
    test_client.set_field('check.balls', doc, 3)
    assert test_client.get_field('check.balls', doc) == 3

def test_vector_name(test_client):
    text_encoder = ViText2Vec(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    test_client.set_name(text_encoder, 'vectorai_text')
    vector_name = test_client._get_vector_name_for_encoding("color", text_encoder, model_list=[text_encoder])
    assert vector_name == "color_vectorai_text_vector_"

def test_vector_name_2(test_client):
    text_encoder = ViText2Vec(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    text_encoder_2 = ViText2Vec(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    test_client.set_name(text_encoder, "vectorai")
    test_client.set_name(text_encoder_2, "vectorai_2")
    vector_name = test_client._get_vector_name_for_encoding("color", text_encoder, model_list=[text_encoder, text_encoder_2])
    assert vector_name == "color_vectorai_vector_"
    vector_name = test_client._get_vector_name_for_encoding("color", text_encoder_2, model_list=[text_encoder, text_encoder_2])
    assert vector_name == 'color_vectorai_2_vector_'

def test_vector_name_same_name(test_client):
    text_encoder = ViText2Vec(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    with pytest.raises(ValueError):
        vector_name = test_client._check_if_multiple_models_have_same_name(models={'color':[text_encoder, text_encoder]})

def test_encode_documents_With_models_using_encode(test_client):
    docs = test_client.create_sample_documents(5)
    text_encoder = ViText2Vec(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    test_client.set_name(text_encoder, "vectorai_text")
    test_client.encode_documents_with_models_using_encode(docs, models={'color': [text_encoder]})
    assert 'color_vectorai_text_vector_' in docs[0].keys()

@pytest.mark.use_client
def test_raises_warning_if_no_id(test_client, test_collection_name):
    docs = test_client.create_sample_documents(10)
    {x.pop('_id') for x in docs}
    with pytest.warns(MissingFieldWarning) as record:
        test_client.insert_documents(test_collection_name, docs)
    assert len(record) > 1
    assert record[1].message.args[0] == test_client.NO_ID_WARNING_MESSAGE

@pytest.mark.use_client
def test_raises_warning_if_only_one_id_is_present(test_client, test_collection_name):
    docs = test_client.create_sample_documents(10)
    {x.pop('_id') for x in docs[1:]}
    with pytest.warns(MissingFieldWarning) as record:
        test_client.insert_documents(test_collection_name, docs)
    assert record[0].message.args[0] == test_client.NO_ID_WARNING_MESSAGE

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

@pytest.mark.parametrize('collection_name',['HIUFE', 'HUIF_;', 'fheuwiHF'])
def test_collection_name_error(test_client, collection_name):
    with pytest.raises(CollectionNameError):
        test_client._typecheck_collection_name(collection_name)

@pytest.mark.parametrize('collection_name', ['fehwu'])
def test_collection_name_not_error(test_client, collection_name):
    test_client._typecheck_collection_name(collection_name)
    assert True
