"""Testing the client.
"""

from vectorai import *


def test_client_login_works(test_username, test_api_key):
    """Testing for the client login.
    """
    client = ViClient(username=test_username, api_key=test_api_key)
    assert True
