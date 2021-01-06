"""
    Add default retry to inserting
"""
import time
from functools import wraps
from ..errors import APIError

def retry(num_of_retries=3, timeout=2):
    """
    Allows the function to retry upon failure. 
    Args:
        num_of_retries: The number of times the function should retry
        timeout: The number of seconds to wait between each retry
    """
    def _retry(func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            for i in range(num_of_retries):
                try:
                    return func(*args, **kwargs)
                # Using general error to avoid any possible error dependencies.
                except Exception as error:
                    time.sleep(timeout)
                    print("Retrying...")
                    if i == num_of_retries - 1:
                        raise error
                    continue
                break
        return function_wrapper
    return _retry

def return_response(response):
    """
    Return error response if the status code != 200.
    """
    if response.status_code != 200:
        raise APIError(response.content)
    return response.json()
