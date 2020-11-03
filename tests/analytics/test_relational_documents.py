"""
    Tests for relational documents.
"""
from vectorai.analytics.relational_documents import *
from vectorai.utils import UtilsMixin
import pytest

def test_vector_operation():
    assert (vector_operation([1, 2, 3], [3, 2, 1]) == [2, 2, 2])

@pytest.mark.parametrize("test_operation, expected_output", [("minus", [0, 0, 0])])
def test_relational_document_creation(test_operation, expected_output):
    mixin_utils = UtilsMixin()
    doc_1 = {'_vector_': [1, 2, 3], 'country': 'Australia'}
    doc_2 = {'_vector_': [1, 2, 3], 'country': 'New Zealand'}
    relational_doc = create_relational_document(doc_1, doc_2, vector_fields=['_vector_'], 
    label_field='country', operation=test_operation)
    assert relational_doc['_vector_'] == expected_output
