import io
import base64
import requests
import pandas as pd
import os
from .write import ViWriteClient
from .utils import decorate_functions_by_argument, set_default_collection
from .errors import LoginError, APIError

class ViClient(ViWriteClient):
    """
        The main Vi client with most of the available read and write methods available to it.

        Parameters:
            username:
                your username for accessing vectorai
            api_key:
                your api key for accessing vectorai
            url:
                url of the deployed vectorai database

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, vectorai_url)
            >>> vi_client.list_collections()
    """

    def __init__(self, username: str=None, api_key: str=None, url: str = "https://api.vctr.ai", verbose: bool = True) -> None:
        super().__init__(username, api_key, url)
        if username is None:
            if 'VI_USERNAME' not in os.environ.keys():
                raise APIError("Specify username of set VI_USERNAME as an environment variable.")
            username = os.environ['VI_USERNAME']
        
        if api_key is None:
            if 'VI_API_KEY' not in os.environ.keys():
                raise APIError("Specify VectorAI API key VI_API_KEY as an environment variable.")
            api_key = os.environ['VI_API_KEY']
        
        self.username = username
        self.api_key = api_key
        self.url = url

        if verbose:
            self.check_login_details()
            print(
                f"Logged in. Welcome {self.username}. To view list of available collections, call list_collections() method."
            )
        
    def check_login_details(self):
        try:
            self.list_collections()
        except:
            raise LoginError("Username, api key or url is incorrect.")


def request_api_key(username: str, email:str, description:str="I'd like to try it out.", referral_code: str="github_referred"):
    """
        Request an api key
        Make sure to save the api key somewhere safe. If you have a valid referral code, you can recieve the api key more quickly.
            
        Args:
            username:
                Username you'd like to create, lowercase only
            email:
                Email you are using to sign up
            description:
                Description of your intended use case
            referral_code:
                The referral code you've been given to allow you to register for an api key before others
    """
    return requests.post(
        url="{}/project/request_api_key".format("https://api.vctr.ai"),
        json={
            "username": username,
            "email": email,
            "referral_code": referral_code,
            "description": description,
        },
    ).json()

@decorate_functions_by_argument(set_default_collection, 'collection_name')
class ViCollectionClient(ViClient):
    """
        The Vi client when you are mainly working with 1 client.

        Args:
            username:
                your username for accessing vecdb
            api_key:
                your api key for accessing vecdb
            url:
                url of the deployed vecdb database
            collection_name:
                The name of the collection

        Example:
            >>> from vectorai.client import ViClient
            >>> vi_client = ViClient(username, api_key, collection_name, vectorai_url)
            >>> vi_client.insert_documents(documents)
    """
    def __init__(self, collection_name: str, username: str, api_key: str, url: str="https://api.vctr.ai", verbose: bool=True) -> None:
        if username is None:
            if 'VI_USERNAME' not in os.environ.keys():
                raise APIError("Specify username of set VI_USERNAME as an environment variable.")
            username = os.environ['VI_USERNAME']
        
        if api_key is None:
            if 'VI_API_KEY' not in os.environ.keys():
                raise APIError("Specify VectorAI API key VI_API_KEY as an environment variable.")
            api_key = os.environ['VI_API_KEY']
        
        self.username = username
        self.api_key = api_key
        self._collection_name = collection_name
        self.url = url
        if verbose:
            self.check_login_details()
            print(
                f"Logged in. Welcome {self.username}. To view list of available collections, call list_collections() method."
            )
            setattr(self, 'decorator_called', False)

    @property
    def collection_name(self) -> str:
        return self._collection_name
    
    @collection_name.setter
    def collection_name(self, value: str) -> None:
        self._collection_name = value
        
    @collection_name.getter
    def collection_name(self) -> str:
        return self._collection_name
