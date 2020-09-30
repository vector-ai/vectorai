import numpy as np
from typing import Any, List
from abc import abstractmethod

class TFHubBase:
    def _vector_operation(self, vectors:List, vector_operation: str = "mean"):
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

class InvalidTFHubURLError(Exception): 
    def __init__(self, supported_urls):
        print(f"Invalid TFhub url for this model, here are the supported urls {supported_urls}")