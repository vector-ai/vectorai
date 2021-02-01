"""
    Add default retry to inserting
"""
import time
import os
from functools import wraps
from ..errors import APIError

def retry(num_of_retries=3, timeout=5):
    """
    Allows the function to retry upon failure. 
    Args:
        num_of_retries: The number of times the function should retry
        timeout: The number of seconds to wait between each retry
    """
    if 'VI_MAX_RETRY' in os.environ.keys():
        num_of_retries = int(os.environ['VI_MAX_RETRY'])
    if 'VI_TIMEOUT' in os.environ.keys():
        timeout = float(os.environ['VI_TIMEOUT'])

    def _retry(func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            for i in range(num_of_retries):
                try:
                    return func(*args, **kwargs)
                # Using general error to avoid any possible error dependencies.
                except ConnectionError as error:
                    time.sleep(timeout)
                    print("Retrying...")
                    if i == num_of_retries - 1:
                        raise error
                    continue
                break
        return function_wrapper
    return _retry

def return_response(response, return_type='json'):
    """
    Return error response if the status code != 200.
    """
    if response.status_code != 200:
        raise APIError(response.content)
    if return_type == 'json':
        return response.json()
    elif return_type == 'content':
        return response.content
