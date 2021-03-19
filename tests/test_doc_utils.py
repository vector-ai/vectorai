"""Testing for document utilities.
"""
import pytest
from vectorai.errors import MissingFieldError

def test_set_field(test_client):
    sample = {}
    test_client.set_field("simple", doc=sample, value=[0, 2])
    assert test_client.get_field("simple", sample) == [0, 2]

def test_set_field_nested(test_client):
    sample = {}
    test_client.set_field('simple.weird.strange', sample, value=3)
    assert test_client.get_field('simple.weird.strange', sample) == 3
    assert sample['simple']['weird']['strange'] == 3

def test_get_field_chunk(test_client):
    sample = {
        'kfc': [{'food': 'chicken'}, {'food': 'prawns'}]}
    assert test_client.get_field('kfc.0.food', sample) == 'chicken'
    assert test_client.get_field('kfc.1.food', sample) == 'prawns'

def test_get_field_chunk_error(test_client):
    sample = {
        'kfc': [{'food': 'chicken'}, {'food': 'prawns'}]}
    with pytest.raises(MissingFieldError):
        test_client.get_field('kfc.food', sample, missing_treatment='raise_error')

def test_get_fields(test_client):
    doc = test_client.create_sample_documents(1)[0]
    assert len(test_client.get_fields(['size.cm', 'size.feet'], doc)) == 2

def test_get_field_across_documents(test_client):
    docs = test_client.create_sample_documents(2)
    values = test_client.get_field_across_documents('color', docs)
    assert len(values) == 2

def test_set_and_get_field_across_documents(test_client):
    docs = test_client.create_sample_documents(5)
    test_client.set_field_across_documents('size.inches', list(range(5)), docs)
    for i, doc in enumerate(docs):
        assert test_client.get_field('size.inches', doc) == i

def test_is_field(test_client):
    """
        Test if it is a field
    """
    docs = test_client.create_sample_documents(10)
    assert test_client.is_field("size", docs[0])
    assert not test_client.is_field("hfueishfuie", docs[0])
    assert test_client.is_field("size.cm", docs[0])
    assert not test_client.is_field("size.bafehui", docs[0])
