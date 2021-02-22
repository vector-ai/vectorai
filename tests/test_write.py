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

def assert_json_serializable(document, temp_json_file="test.json"):
    """Assert that an document is json serializable and is the same after loading back into Python.
    """
    with open(temp_json_file, "w") as f:
        json.dump(document, f)
    return_document = json.load(open(temp_json_file, "r"))
    os.remove(temp_json_file)
    assert return_document == document

class TestInsert:
    @pytest.mark.use_client
    def test_insert_documents_simple_and_collection_stats_match(self, test_client, test_collection_name):
        """
            Testing for simple document insertion
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        test_client.insert_documents(test_collection_name, sample_documents)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_without_id_fields(self, test_client, test_collection_name):
        """
            Test inserting documents if they do not have an ID field.
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Remove the ID fields
        {x.pop('_id') for x in sample_documents}
        test_client.insert_documents(test_collection_name, sample_documents)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_without_id_fields_with_overwrite(self, test_client, test_collection_name):
        """
            Test inserting documents if they do not have an ID field.
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Remove the ID fields
        {x.pop('_id') for x in sample_documents}
        with pytest.warns(MissingFieldWarning):
            test_client.insert_documents(test_collection_name, sample_documents, overwrite=True)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_when_id_is_not_a_string(self, test_client, test_collection_name):
        """
            Test inserting documents when ID is not a string
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Create integer IDs strings
        {x.update({'_id': int(x['_id'])}) for x in sample_documents}
        test_client.insert_documents(test_collection_name, sample_documents, overwrite=False)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

    @pytest.mark.use_client
    def test_inserting_documents_when_id_is_not_a_string_with_overwrite(self, test_client, test_collection_name):
        """
            Test inserting documents when ID is not a string
        """
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        sample_documents = test_client.create_sample_documents(10)
        # Create integer IDs strings
        {x.update({'_id': int(x['_id'])}) for x in sample_documents}
        test_client.insert_documents(test_collection_name, sample_documents, overwrite=True)
        time.sleep(10)
        assert test_client.collection_stats(test_collection_name)['number_of_documents'] == 10
        test_client.delete_collection(test_collection_name)
        time.sleep(3)

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
        time.sleep(10)
        assert True


    @pytest.mark.use_client
    def test_edit_document(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            edits = {
                "_id": "1",
                "location": "Paris"
            }
            client.edit_document(
                collection_name=test_collection_name, edits=edits
            )
            time.sleep(2)
            doc = client.id(test_collection_name, document_id="1")
            assert doc["location"] == "Paris"

    @pytest.mark.use_client
    def test_create_filter(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            doc = {
                'location': "Paris"
            }
            client.insert_document(test_collection_name, doc)
            results = test_client.filters(
                test_collection_name,
                test_client.create_filter_query(test_collection_name, 'location', 'contains', 'paris'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_create_filter_2(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            doc = {
                'location': "Paris"
            }
            client.insert_document(test_collection_name, doc)
            results = test_client.filters(
                test_collection_name,
                test_client.create_filter_query(
                    test_collection_name, 'location', 'exact_match', 'Paris'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_create_filter_3(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name) as client:
            results = test_client.filters(test_collection_name,
            test_client.create_filter_query(test_collection_name, 'size.feet', '<=', '31'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_create_filter_4(self, test_client, test_collection_name):
        with TempClientWithDocs(test_client, test_collection_name):
            results = test_client.filters(test_collection_name,
            test_client.create_filter_query(test_collection_name, 'insert_date_', '>=', '2020-01-01'))
            assert len(results) > 0

    @pytest.mark.use_client
    def test_edit_documents(self, test_client, test_collection_name):
        """Test adding of an attribute
        """
        with TempClientWithDocs(test_client, test_collection_name):
            edits = [
                {"_id": "2", "location": "Sydney",},
                {"_id": "1", "location": "New York",},
            ]
            test_client.edit_documents(test_collection_name, edits)
            doc = test_client.id(test_collection_name, document_id="2")
            assert doc["location"] == "Sydney"
            doc = test_client.id(test_collection_name, document_id="1")
            assert doc['location'] == 'New York'

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
def test_multiprocess_with_collection_client(test_collection_client, test_collection_name):
    NUM_OF_DOCUMENTS_INSERTED = 100
    if test_collection_client.collection_name in test_collection_client.list_collections():
        test_collection_client.delete_collection()
        time.sleep(5)
    documents = test_collection_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    results = test_collection_client.insert_documents(documents, workers=5)
    time.sleep(10)
    assert len(results['failed_document_ids']) == 0
    assert test_collection_client.collection_name in test_collection_client.list_collections()
    assert test_collection_client.collection_stats()['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED
    test_collection_client.delete_collection()

@pytest.mark.use_client
def test_multiprocess__with_error_with_collection_client(test_collection_client):
    NUM_OF_DOCUMENTS_INSERTED = 100
    if test_collection_client.collection_name in test_collection_client.list_collections():
        test_collection_client.delete_collection()
        time.sleep(5)
    documents = test_collection_client.create_sample_documents(NUM_OF_DOCUMENTS_INSERTED)
    documents.append({
        '_id': 9993,
        'color': np.nan
    })
    # This should result in 1 failure
    results = test_collection_client.insert_documents(documents, workers=5, overwrite=True)
    time.sleep(10)
    assert len(results['failed_document_ids']) == 1
    assert test_collection_client.collection_name in test_collection_client.list_collections()
    assert test_collection_client.collection_stats()['number_of_documents'] == NUM_OF_DOCUMENTS_INSERTED

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
    id_document = test_client.id(test_collection_name, TEST_ID)
    test_client.set_field('test.field', id_document, 'stranger')
    docs[3] = id_document
    print(docs[3])
    docs[3].update({'_id': '3'})
    response = test_client.insert_documents(test_collection_name, docs[3:5], workers=1,
    overwrite=True)
    id_document = test_client.id(test_collection_name, TEST_ID)
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
    id_document = test_client.id(test_collection_name, TEST_ID)
    test_client.set_field('test.field', id_document, 'stranger')
    docs[3] = id_document
    docs[3].update({'_id': '3'})
    response = test_client.insert_documents(test_collection_name, docs[3:5], workers=1,
    overwrite=False)
    id_document = test_client.id(test_collection_name, TEST_ID)
    with pytest.raises(MissingFieldError):
        test_client.get_field('test.field', id_document)
    time.sleep(5)
    test_client.delete_collection(test_collection_name)

@pytest.mark.use_client
def test_multiprocess_overwrite_collection_client(test_collection_client, test_collection_name):
    if test_collection_client.collection_name in test_collection_client.list_collections():
        test_collection_client.delete_collection()
        time.sleep(5)
    NUM_OF_DOCS = 10
    docs = test_collection_client.create_sample_documents(NUM_OF_DOCS)
    test_collection_client.insert_documents(docs[0:5], workers=1, overwrite=False)
    # For document with id '3'
    TEST_ID = '3'
    id_document = test_collection_client.id(TEST_ID)
    test_collection_client.set_field('test.field', id_document, 'stranger')
    docs[3] = id_document
    docs[3].update({'_id': '3'})
    response = test_collection_client.insert_documents(docs[3:5], workers=1,
    overwrite=True)
    id_document = test_collection_client.id(TEST_ID)
    assert test_collection_client.get_field('test.field', id_document) == 'stranger'
    time.sleep(5)
    test_collection_client.delete_collection()

@pytest.mark.use_client
def test_multiprocess_not_overwrite_collection_client(test_collection_client, test_collection_name):
    NUM_OF_DOCS = 10
    docs = test_collection_client.create_sample_documents(NUM_OF_DOCS)
    test_collection_client.insert_documents(docs[0:5], workers=1, overwrite=False)
    # For document with id '3'
    TEST_ID = '3'
    id_document = test_collection_client.id(TEST_ID)
    test_collection_client.set_field('test.field', id_document, 'stranger')
    docs[3] = id_document
    docs[3].update({'_id': '3'})
    response = test_collection_client.insert_documents(docs[3:5], workers=1,
    overwrite=False)
    id_document = test_collection_client.id(TEST_ID)
    with pytest.raises(MissingFieldError):
        test_collection_client.get_field('test.field', id_document)
    time.sleep(5)
    test_collection_client.delete_collection()

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

@pytest.mark.use_client
def test_edit_documents(test_client, test_collection_name):
    with TempClientWithDocs(test_client, test_collection_name, 100) as client:
        edits = test_client.create_sample_documents(100)
        {x.update({'favorite_singer': 'billie eilish'}) for x in edits}
        response = client.edit_documents(test_collection_name, edits)
        assert response['edited_successfully'] == len(edits)
        # Retrieve the documents 
        docs = client.retrieve_documents(test_collection_name, 
        include_fields=['favorite_singer'], page_size=1)['documents']
        for doc in docs:
            assert doc['favorite_singer'] == 'billie eilish' 

@pytest.mark.parametrize('collection_name',['HIUFE', 'HUIF_;', 'fheuwiHF'])
def test_collection_name_error(test_client, collection_name):
    with pytest.raises(CollectionNameError):
        test_client._typecheck_collection_name(collection_name)

@pytest.mark.parametrize('collection_name', ['fehwu'])
def test_collection_name_not_error(test_client, collection_name):
    test_client._typecheck_collection_name(collection_name)
    assert True
