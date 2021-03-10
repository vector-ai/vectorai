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
