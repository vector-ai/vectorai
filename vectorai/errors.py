"""Errors
"""
class APIError(Exception):
    """Base error class for all errors in library
    """

    def __init__(self, response_message: str=None):
        """
        The main Vi  base error.

        Args:
            response_message: THe error message

        Example:
            >>> raise APIError("Missing ____.")
        """
        self.response_message = response_message

class MissingFieldWarning(APIError, UserWarning):
    """
        Warning for missing field. Used for checking collection schema
        upon insertion.
    """
    pass

class MissingFieldError(APIError):
    """
        Error in case the field is missing from a document.
        Used for when a specific field is missing.
    """
    pass

class LoginError(APIError):
    """
    Login Error
    """
    pass

class CollectionNameError(APIError):
    """
    Collection Name Error
    """
    pass
