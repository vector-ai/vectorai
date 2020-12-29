"""
Global testing variables.
"""
import pytest
import os
import random
import string
import datetime
import numpy as np
from vectorai.client import *
from vectorai.models.deployed import ViText2Vec

def pytest_addoption(parser):
    parser.addoption(
        "--use_client", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--use_client"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --use_client option to run")
    for item in items:
        if "use_client" in item.keywords:
            item.add_marker(skip_slow)

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(length))

@pytest.fixture
def test_username():
    return os.environ['VI_USERNAME']


@pytest.fixture
def test_api_key():
    return os.environ['VI_API_KEY']


@pytest.fixture
def test_client(test_username, test_api_key):
    """Testing for the client login.
    """
    client = ViClient(username=test_username, api_key=test_api_key)
    return client

@pytest.fixture(scope='class')
def test_collection_name():
    return "test_colour_col_" + str(get_random_string(3))

@pytest.fixture
def test_collection_client(test_username, test_api_key, test_collection_name):
    """Testing for the client login.
    """
    client = ViCollectionClient(username=test_username, api_key=test_api_key, collection_name=test_collection_name)
    return client


@pytest.fixture
def test_vector_field():
    return "item_vector_"


@pytest.fixture
def test_id_field():
    return "_id"

@pytest.fixture
def sample_documents():
    sample_documents = [
        {
            "name": "Bob",
            "color": "Orange",
            "team": "los angeles lakers"
        },
        {
            "name": "William",
            "color": "Yellow",
            "team": "miami heat"
        },
        {
            "name": "James Patterson",
            "color": "Blue",
            "team": "Charlotte Bobcats"
        }
    ]
    return sample_documents


@pytest.fixture
def test_text_encoder():
    """
        Text Encoder
    """
    model = ViText2Vec(os.environ['VI_USERNAME'], os.environ['VI_API_KEY'])
    return model

@pytest.fixture
def test_create_collection_for_join(test_client):
    """
        Delete and create new collection for join
    """
    NAMES = ("Jordan", "Georgia", "Ben", "Tom")
    CARBRANDS = ("Ford", "Tesla", "Honda")
    INSURANCE_TYPE = ("Comprehensive", "3rd Party", "Theft", "FIRE")

    number_of_vecs = 10
    vec_dimension = 10

    vecs = np.random.random((number_of_vecs, vec_dimension)).astype('float32')
    person_docs = [{
        '_id': v,
        'person_rf_vector_': vecs[v].tolist(),
        'name': random.choice(NAMES),
        'car_model': random.choice(CARBRANDS) + '-' + str(random.randrange(10)),
        'insurance_type': random.choice(INSURANCE_TYPE),
        'date': datetime.datetime.now().isoformat()
    } for v in range(len(vecs))]

    test_client.delete_collection('person')
    test_client.create_collection('person')
    test_client.insert_documents('person',person_docs)


    car_docs = []
    for v in range(len(CARBRANDS)):
        for r in range(10):
            car_docs.append({
                '_id': v*100+r,
                'car_rf_vector_': vecs[v].tolist(),
                'model': CARBRANDS[v] + '-' + str(r),
                'brand': CARBRANDS[v],
                'year': random.randrange(1990, 2020),
                'date': datetime.datetime.now().isoformat()
            })

    test_client.delete_collection('car')
    test_client.create_collection('car')
    test_client.insert_documents('car',car_docs)
