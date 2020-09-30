import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import numpy as np
import traceback
import imageio
from typing import Any, List
from .base import TFHubBase, InvalidTFHubURLError

USE_URLS = [
    "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3",
    "https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3",
    "https://tfhub.dev/google/universal-sentence-encoder/4",
    "https://tfhub.dev/google/universal-sentence-encoder-large/5",
]

class UseText2Vec(TFHubBase):
    def __init__(self, model_url:str='https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3'):
        if model_url not in USE_URLS:
            raise InvalidTFHubURLError
        self.model_url = model_url
        self.model = hub.load(self.model_url)
        self._name = self.model_url.replace('https://tfhub.dev/google/', '').replace('/', '_')
        self.vector_length = 2048

    def encode(self, data:Any):
        try:
            return self.model([data]).numpy()[0].tolist()
        except:
            print("something went wrong with encoding an audio, we are imputing it with a vector of [1e-7]*vector_length")
            traceback.print_exc()
            return [1e-7]*self.vector_length

    def bulk_encode(self, data:List[str], threads:int=10, compress_method:str='mean', chunks:int=100): #can consider compress in the future
        return [self.encode(i) for c in self._chunks(data, chunks) for i in c]
