import numpy as np
from abc import abstractmethod


class ViDeployedModel:
    def __init__(self, username, api_key, url="https://api.vctr.ai", collection_name="base"):
        self.username = username
        self.api_key = api_key
        self.url = url
        self.collection_name = collection_name
        self._name = "default"
    
    def _vector_operation(self, vectors, vector_operation: str = "mean"):
        """
            Creates a vector operation based on the model
        """
        vector_operation = vector_operation.lower()
        if vector_operation == "mean" or vector_operation=="average":
            return np.mean(vectors, axis=0).tolist()
        elif vector_operation == 'minus':
            if len(vectors) > 2:
                raise ValueError("More than 2 vectors.")
            return np.subtract(vectors[0], vectors[1]).tolist()
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
