import io
import base64
import requests
from .base import ViDeployedModel


class ViImage2Vec(ViDeployedModel):
    def encode(self, image):
        return requests.get(
            url="{}/collection/encode_image".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": self.collection_name,
                "image_url": image,
            },
        ).json()

    @property
    def __name__(self):
        if self._name is None:
            return "deployed_image"
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value


class ViImageArray2Vec(ViDeployedModel):
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

    def encode(self, images):
        return _vector_operation(
            [
                requests.get(
                    url="{}/collection/encode_image".format(self.url),
                    params={
                        "username": self.username,
                        "api_key": self.api_key,
                        "collection_name": self.collection_name,
                        "image_url": image,
                    },
                ).json()
                for image in images
            ],
            vector_operation=self.vector_operation,
        )

    @property
    def __name__(self):
        if self._name is None:
            return "deployed_image_array"
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value
