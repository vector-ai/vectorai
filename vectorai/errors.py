"""Errors
"""


class APIError(Exception):
    """Base error class for all errors in library
    """

    def __init__(self, response_message: str):
        """
        The main Vi  base error.

        Args:
            response_message: THe error message

        Example:
            >>> raise APIError("Missing ____.")
        """
        self.response_message = response_message

class LoginError(APIError):
    """
    Login Error
    """
    pass