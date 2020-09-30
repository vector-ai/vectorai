import io
import librosa
import soundfile as sf
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import traceback
import tempfile, shutil, os
from urllib.request import urlopen, Request
from urllib.parse import quote
from typing import Any, List
from .base import TFHubBase, InvalidTFHubURLError

class TrillAudio2Vec(TFHubBase):
    def __init__(self, layer:str='embedding', distilled:bool=False):  # layer19
        if distilled:
            self.model_url = 'https://tfhub.dev/google/nonsemantic-speech-benchmark/trill-distilled/1'
        else:
            self.model_url = 'https://tfhub.dev/google/nonsemantic-speech-benchmark/trill/3'
        self.model = hub.load(self.model_url)
        self._name = self.model_url.replace('https://tfhub.dev/google/', '').replace('/', '_')
        self.vector_length = 512
        self.sample_rate = 16000
        self.layer = layer

    def encode(self, data:Any, compress_method:str='mean'):
        try:
            encodings = self.model(samples=np.array(self.read_audio(data, self.sample_rate)), sample_rate=self.sample_rate)[self.layer]
            return self._vector_operation(encodings, compress_method)
        except Exception as e:
            print("something went wrong with encoding an audio, we are imputing it with a vector of [1e-7]*vector_length")
            traceback.print_exc()
            return [1e-7]*self.vector_length

    def bulk_encode(self, data:List[Any], compress_method:str='mean', chunks:int=1000, threads:int=10):
        return [self.encode(i, compress_method=compress_method) for i in data]

    def read_audio(self, audio, new_sampling_rate:int):
        if type(audio) == str:
            if 'http' in audio:
                fd, fp = tempfile.mkstemp()
                os.write(fd, urlopen(Request(quote(audio, safe=':/?*=\''), headers={'User-Agent' : "Magic Browser"})).read())
                if '.mp3' in audio:
                    data, sampling_rate = librosa.load(fp, dtype='float32')
                else:
                    data, sampling_rate = sf.read(fp, dtype='float32')
                os.close(fd)
            else:
                data, sampling_rate = sf.read(audio, dtype='float32')
        elif type(audio) == bytes:
            data, sampling_rate = sf.read(io.BytesIO(audio), dtype='float32')
        elif type(audio) == io.BytesIO:
            data, sampling_rate = sf.read(audio, dtype='float32')
        return np.array(librosa.resample(data.T, sampling_rate, new_sampling_rate))