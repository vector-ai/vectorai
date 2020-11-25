"""
    Test for models.
"""

import pytest
from vectorai.models import ViDeployedModel

def test_operations_sum(test_text_encoder):
    vectors = [[1, 2], [2, 3]]
    assert [3, 5] == test_text_encoder._vector_operation(vectors, vector_operation="sum")

def test_operations_minus(test_text_encoder):
    vectors = [[1, 2], [2, 3]]
    assert [-1, -1] == test_text_encoder._vector_operation(vectors, vector_operation="minus")

def test_operations_mean(test_text_encoder):
    vectors = [[1, 2], [2, 3]]
    assert [1.5, 2.5] == test_text_encoder._vector_operation(vectors, vector_operation="mean")

def test_operations_max(test_text_encoder):
    vectors = [[1, 2], [2, 3]]
    assert [2, 3] == test_text_encoder._vector_operation(vectors, vector_operation="max")

def test_operations_min(test_text_encoder):
    vectors = [[1, 2], [2, 3]]
    assert [1, 2] == test_text_encoder._vector_operation(vectors, vector_operation="min")

def test_operations_min_with_error(test_text_encoder):
    with pytest.raises(ValueError):
        vectors = vectors = [[1, 2], [2, 3], [2, 4]]
        test_text_encoder._vector_operation(vectors, vector_operation='minus')
