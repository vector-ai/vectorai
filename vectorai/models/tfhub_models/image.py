import io
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import traceback
import imageio
from typing import Any, List
from urllib.request import urlopen, Request
from urllib.parse import quote
from .base import TFHubBase, InvalidTFHubURLError

BIT_URLS = [
    "https://tfhub.dev/google/bit/s-r50x1/1",
    "https://tfhub.dev/google/bit/s-r50x3/1",
    "https://tfhub.dev/google/bit/s-r101x1/1",
    "https://tfhub.dev/google/bit/s-r101x3/1",
    "https://tfhub.dev/google/bit/s-r152x4/1",
    "https://tfhub.dev/google/bit/m-r50x1/1",
    "https://tfhub.dev/google/bit/m-r50x3/1",
    "https://tfhub.dev/google/bit/m-r101x1/1",
    "https://tfhub.dev/google/bit/m-r101x3/1",
    "https://tfhub.dev/google/bit/m-r152x4/1",
]

class BitImage2Vec(TFHubBase):
    def __init__(self, model_url="https://tfhub.dev/google/bit/s-r50x1/1"):
        if model_url not in BIT_URLS:
            raise InvalidTFHubURLError
        self.model_url = 'https://tfhub.dev/google/bit/m-r50x1/1'
        self.model = hub.load(self.model_url)
        self._name = self.model_url.replace('https://tfhub.dev/google/', '').replace('/', '_')
        self.vector_length = 2048

    def encode(self, data:Any):
        try:
            return self.model([self.read_image(data)]).numpy()[0].tolist()
        except:
            print("something went wrong with encoding an image, we are imputing it with a vector of [1e-7]*vector_length")
            traceback.print_exc()
            return [1e-7]*self.vector_length

    def bulk_encode(self, data:List[Any], threads=10, compress_method='mean', chunks=100): #can consider compress in the future
        if 'http' in data[0]:
            print()
            image_folder = ''
        else:
            print()
            image_folder = ''
        image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
        image_data = image_generator.flow_from_directory(image_folder, target_size=(224, 224))
        encodings = []
        for image_batch, label_batch in image_data:
            encodings += self.model(image_batch).numpy().tolist()
        return [self.encode(i) for c in self._chunks(data, chunks) for i in c]

    def read_image(self, image, width=0, height=0):
        if type(image) == str:
            if 'http' in image:
                b = io.BytesIO(urlopen(Request(quote(image, safe=':/?*=\''), headers={'User-Agent' : "Mozilla/5.0"})).read())
            else:
                b = image
        elif type(image) == bytes:
            b = io.BytesIO(image)
        elif type(audio) == io.BytesIO:
            b = image
        try:
            return np.array(imageio.imread(b, pilmode="RGB"))
        except:
            return np.array(imageio.imread(b)[:,:,:3])