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
def test_multiprocess_insert(test_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 10
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
        time.sleep(10)
    documents = test_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    results = test_client.insert_documents(test_collection_name, documents, workers=5, overwrite=False)
    time.sleep(10)
    assert len(results['failed_document_ids']) == 0
    assert test_collection_name in test_client.list_collections()
    assert test_client.collection_stats(test_collection_name)['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_insert_with_error(test_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 100
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
    documents = test_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    documents.append({
        '_id': '9993',
        'color': np.nan
    })

    # This should result in 1 failure
    results = test_client.insert_documents(test_collection_name, documents, workers=5, overwrite=False)
    time.sleep(10)
    assert len(results['failed_document_ids']) == 1
    assert test_collection_name in test_client.list_collections()
    assert test_client.collection_stats(test_collection_name)['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_insert_with_error_with_overwrite(test_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 100
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
        time.sleep(5)
    documents = test_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    documents.append({
        '_id': '9993',
        'color': np.nan
    })

    # This should result in 1 failure
    results = test_client.insert_documents(test_collection_name, documents, workers=5, overwrite=True)
    time.sleep(10)
    assert len(results['failed_document_ids']) == 1
    assert test_collection_name in test_client.list_collections()
    assert test_client.collection_stats(test_collection_name)['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_with_overwrite(test_client, test_collection_name):
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
        time.sleep(5)
    NUM_OF_DOCS = 10
    docs = test_client.create_sample_documents(NUM_OF_DOCS)
    test_client.insert_documents(test_collection_name, docs[0:5], workers=1, overwrite=False)
    response = test_client.insert_documents(test_collection_name, docs[3:5], workers=1,
    overwrite=True)
    assert response['inserted_successfully'] == 2

@pytest.mark.use_client
def test_multiprocess_with_overwrite_insert(test_client, test_collection_name):
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
        time.sleep(5)
    NUM_OF_DOCS = 10
    docs = test_client.create_sample_documents(NUM_OF_DOCS)
    test_client.insert_documents(test_collection_name, docs[0:5], workers=1, overwrite=False)
    response = test_client.insert_documents(test_collection_name, docs[3:5], workers=1,
    overwrite=True)
    assert response['inserted_successfully'] == 2

@pytest.mark.use_client
def test_multiprocess_overwrite(test_client, test_collection_name):
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
        time.sleep(5)
    NUM_OF_DOCS = 100
    docs = test_client.create_sample_documents(NUM_OF_DOCS)
    test_client.insert_documents(test_collection_name, docs[0:5], workers=1, overwrite=False)
    # For document with id '3'
    TEST_ID = '3'
    id_document = test_client.id(collection_name=test_collection_name, document_id=TEST_ID)
    test_client.set_field('test.field', id_document, 'stranger')
    docs[3] = id_document
    print(docs[3])
    docs[3].update({'_id': '3'})
    response = test_client.insert_documents(test_collection_name, docs[3:5], workers=1,
    overwrite=True)
    id_document = test_client.id(collection_name=test_collection_name, document_id=TEST_ID)
    assert test_client.get_field('test.field', id_document) == 'stranger'
    time.sleep(5)
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_not_overwrite(test_client, test_collection_name):
    if test_collection_name in test_client.list_collections():
        test_client.delete_collection(test_collection_name)
        time.sleep(5)
    NUM_OF_DOCS = 100
    docs = test_client.create_sample_documents(NUM_OF_DOCS)
    test_client.insert_documents(test_collection_name, docs[0:5], workers=1, overwrite=False)
    # For document with id '3'
    TEST_ID = '3'
    id_document = test_client.id(collection_name=test_collection_name, document_id=TEST_ID)
    test_client.set_field('test.field', id_document, 'stranger')
    docs[3] = id_document
    docs[3].update({'_id': '3'})
    response = test_client.insert_documents(test_collection_name, docs[3:5], workers=1,
    overwrite=False)
    id_document = test_client.id(collection_name=test_collection_name, document_id=TEST_ID)
    with pytest.raises(MissingFieldError):
        test_client.get_field('test.field', id_document)
    time.sleep(5)
    test_client.delete_collection(test_collection_name)
