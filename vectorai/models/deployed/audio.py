import io
import base64
import requests
from .base import ViDeployedModel


class ViAudio2Vec(ViDeployedModel):
    def encode(self, audio):
        return requests.get(
            url="{}/collection/encode_audio".format(self.url),
            params={
                "username": self.username,
                "api_key": self.api_key,
                "collection_name": self.collection_name,
                "audio_url": audio,
            },
        ).json()

    @property
    def __name__(self):
        if self._name is None:
            return "vectorai_audio"
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value


class ViAudioArray2Vec(ViDeployedModel):
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

    def encode(self, audios):
        return _vector_operation(
            [
                requests.get(
                    url="{}/collection/encode_audio".format(self.url),
                    params={
                        "username": self.username,
                        "api_key": self.api_key,
                        "collection_name": self.collection_name,
                        "audio_url": audio,
                    },
                ).json()
                for audio in audios
            ],
            vector_operation=self.vector_operation,
        )

    @property
    def __name__(self):
        if self._name is None:
            return "vectorai_audio_array"
        return self._name

    @__name__.setter
    def __name__(self, value):
        self._name = value
