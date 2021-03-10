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

def test__write_document_nested_field():
    sample = {"this": {}}
    ViWriteClient.set_field("this.is", doc=sample, value=[0, 2])
    assert sample["this"]["is"] == [0, 2]

def test__write_document_nested_field_2():
    sample = {"this": {"is": {}}}
    ViWriteClient.set_field("this.is", doc=sample, value=[0, 2])
    assert sample["this"]["is"] == [0, 2]

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
