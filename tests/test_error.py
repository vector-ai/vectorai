"""
    Testing for Errors
"""
import pytest
from vectorai.errors import APIError

def test_api_error(test_client):
    response = {'status': "error", "message": "This is a test error."}
    with pytest.raises(APIError):
        test_client._raise_error(response)
