import numpy as np
from abc import abstractmethod


class ViDeployedModel:
    def __init__(self, username, api_key, url=None, collection_name="base"):
        self.username = username
        self.api_key = api_key
        if url:
            self.url = url
        else:
            self.url = "https://api.vctr.ai"
        self.collection_name = collection_name
        self._name = "default"

    def _vector_operation(self, vectors, vector_operation: str = "mean"):
        if vector_operation == "mean":
            return np.mean(vectors, axis=0).tolist()
        elif vector_operation == "sum":
            return np.sum(vectors, axis=0).tolist()
        elif vector_operation == "min":
            return np.min(vectors, axis=0).tolist()
        elif vector_operation == "max":
            return np.max(vectors, axis=0).tolist()
        else:
            return np.mean(vectors, axis=0).tolist()

    @abstractmethod
    def __name__(self):
        pass
