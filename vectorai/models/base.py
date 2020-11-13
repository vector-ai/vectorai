"""Base class for models
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Union
import json
import gc
import os
from appdirs import *
from ..client import ViWriteClient

class _Vi2Vec(ViWriteClient):
    """
    Abstract class for text models. We inherit from the base class to make use of the ability to write 
    to nested dictionaries and other utilities that will be helpful.
    """

    def chunk(self, documents, chunk_size=20):
        return ViWriteClient.chunk(documents, chunk_size)

    def init_tpu(self):
        """
            Initialise TPU for training a model.

            Example::

                >>> from vectorai.client import Transformer2Vec
                >>> model = Transformer2Vec
                >>> model.init_tpu()
        """
        try:
            tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
            print("Running on TPU ", tpu.cluster_spec().as_dict()["worker"])
            IS_TPU = True
            tf.config.experimental_connect_to_cluster(tpu)
            tf.tpu.experimental.initialize_tpu_system(tpu)
            self.tpu_strategy = tf.distribute.experimental.TPUStrategy(tpu)
        except:
            pass
    
    @staticmethod
    def is_json_serializable(document: dict):
        """
            Check to ensure a document is JSON serializable.
            
            Example::

                >>> from vectorai.client import Transformer2Vec
                >>> sample_doc = {'test': 'hi'}
                >>> Transformer2Vec.is_json_serializable(sample_doc)
                >>> model.init_tpu()
        """
        assert isinstance(document, dict), "Check only 1 item!"
        test_json = user_data_dir("test_vectorai", "test.json")

        with open(test_json, "w"):
            json.dump(test_json)

        with open(test_json) as f:
            check_json = json.load(f)
        os.remove(test_json)
        
        assert check_json == document, (
            "This will not upload correctly. Please ensure all items "
            + "in the dictionary are lists/floats/ints/strings."
        )
        print("Checked! Feel free to upload!")

    @abstractmethod
    def encode(x):
        """An abstract method to specify the encode method.
        """
        pass


class ViText2Vec(_Vi2Vec):
    """Abstract class for text models.
    """

    @abstractmethod
    def encode_text(self, text: Union[str, Dict]) -> List[float]:
        """Encodes either string or a document.
        """
        pass

    def encode(self, text: str):
        """
            Text to vector.
            
            Args:
                text:
                    Text to encode.
            
            Example::

                >>> from vectorai.client import Transformer2Vec
                >>> sample_doc = {'test': 'hi'}
                >>> model_transformer = Transformer2Vec('distilbert')
                >>> model_transformer.encode("Riemann Sums.")
        """
        return self.encode_text(text=text)

    def bulk_encode(self, *args, **kwargs):
        return self.bulk_encode_text(*args, **kwargs)

    def bulk_encode_text(
        self,
        documents: Union[List[str], List[Dict]],
        document_fields: str = None,
        vector_output_field: str = None,
        chunk_size: int = 10,
    ) -> List[float]:
        """
            Encodes either a list of strings or a list of documents. This can be over-ridden if bulk-encoding is supported
            outside of list comprehension.
            Currently only supports 1 input text field.
            Bulk encoding text assumes that bulk-encoding is best done via list comprehension of encode_text.

            Args:
                documents:
                    A list of Python dictionaries
                document_fields
                    The fields to encode
                vector_output_field:
                    The name of the vector output
                chunk_size (batch size): 
                    The number of documents to encode.

            Example::

                >>> from vectorai.client import Transformer2Vec
                >>> sample_docs = [{'name': 'bert', 'age": 10}, {'name': 'elmo', 'age': 15}]
                >>> model_transformer = Transformer2Vec('distilbert')
                >>> model_transformer.bulk_encode(sample_docs, "name")
        
        """
        if vector_output_field is None:
            vector_output_field = document_fields + '_vector_'
        
        if isinstance(documents[0], str):
            assert (
                document_fields is None
            ), "You cannot have an input text field if you are just feeding in a list of documents."
            assert (
                vector_output_field is None
            ), "You cannot have a vector output field if you are feeding i- Overfitting does not seem to provide good results. "
            # typechecking to ensure correct input is fed in.
            all_vectors = []
            for chunk in self.chunk(documents, chunk_size=chunk_size):
                all_vectors.append(self.encode_text(chunk))
            return all_vectors

        if isinstance(documents[0], dict):
            assert (
                document_fields is not None
            ), "You need a text input field if you are not feeding in at a document level."
            assert (
                vector_output_field is not None
            ), "You need a vector output field if you are feeding in at a document level."
            for chunk in self.chunk(documents, chunk_size=chunk_size):
                # List comprehension of the text encoding methodology.
                vectors = [
                    self.encode_text(document=x, document_fields=document_fields)
                    for x in chunk
                ]
                [
                    x.update({vector_output_field: vector})
                    for x, vector in list(zip(chunk, vectors))
                ]
                del vectors
                gc.collect()
            print("Finished updating documents with additional field.")
            return
        raise ValueError(
            "Unsure of how to bulk encode. Please write custom encoding methodology"
        )


class ViImage2Vec(_Vi2Vec):
    """Abstract class for image models.
    """

    @abstractmethod
    def encode_image(self, image) -> List[float]:
        pass

    @abstractmethod
    def bulk_encode_image(self, images):
        pass


class ViAudio2Vec(_Vi2Vec):
    """Abstract class for audio models.
    """

    @abstractmethod
    def encode_audio(self, audio) -> List[float]:
        pass

    @abstractmethod
    def bulk_encode_audio(self, audio):
        pass
