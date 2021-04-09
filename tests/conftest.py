"""
Global testing variables.
"""
import pytest
import os
from vectorai.client import ViClient
from vectorai.analytics.client import ViAnalyticsClient
from vectorai.models.deployed import ViText2Vec
import random
import string

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
    return ViClient(username=test_username, api_key=test_api_key,
        url="https://vectorai-development-api-vectorai-test-api.azurewebsites.net/")

@pytest.fixture(scope='class')
def test_collection_name():
    return "test_colour_col_" + str(get_random_string(3))

# @pytest.fixture
# def test_collection_client(test_username, test_api_key, test_collection_name):
#     """Testing for the client login.
#     """
#     client = ViCollectionClient(username=test_username, api_key=test_api_key, collection_name=test_collection_name)
#     return client

@pytest.fixture
def test_analytics_client(test_username, test_api_key):
    return ViClient(username=test_username, api_key=test_api_key)

@pytest.fixture
def test_vector_field():
    return "item_vector_"

@pytest.fixture
def document_vector_fields():
    return ['color_vector_', 'color_2_vector_']

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
