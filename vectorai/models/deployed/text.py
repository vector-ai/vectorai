import io
import base64
import requests
import numpy as np
from typing import List
from .base import ViDeployedModel


class ViText2Vec(ViDeployedModel):
    def encode(self, text: str):
        """
            Convert text to vectors.
        """
        return requests.get(
            url="{}/collection/encode_text".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": self.collection_name,
                "text": text,
            },
        ).json()

    def bulk_encode(self, texts: List[str]):
        """
            Bulk convert text to vectors
        """
        return requests.get(
            url="{}/collection/bulk_encode_text".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": self.collection_name,
                "texts": texts,
            }
        ).json()

    @property
    def __name__(self):
        if self._name is None:
            return "vectorai_text"
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value


class ViTextArray2Vec(ViDeployedModel):
    def __init__(
        self,
        username,
        api_key,
        url=None,
        collection_name="base",
        vector_operation: str = "mean",
    ):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"
        self.collection_name = collection_name
        self.vector_operation = vector_operation

    def encode(self, texts):
        return self._vector_operation(
            requests.get(
                url="{}/collection/bulk_encode_text".format(self.url),
                params={
                    "username": self.username,
                    "api_key": self.api_key,
                    "collection_name": self.collection_name,
                    "texts": texts,
                }
            ).json(),
            vector_operation=self.vector_operation,
        )

    @property
    def __name__(self):
        if self._name is None:
            return "vectorai_text_array"
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value
