"""Vi Dimensionality Reduction
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from ..write import ViWriteClient


class ViDimensionalityReductionBase(ViWriteClient):
    """
    Base class for dimensionality reduction.
    
    Example:
        >>> class IVISDimensionalityReduction(ViDimensionalityReductionBase):
        >>>     def __init__(self, batch_size=120, k=15, embedding_dims=2):
        >>>         self.scaler = MinMaxScaler()
        >>>         self.model = Ivis(embedding_dims=embedding_dims, k=k, batch_size=batch_size)
        >>>     def fit_transform(self, documents, field_vector):
        >>>           if isinstance(documents[0], dict):
        >>>             if 'documents' in documents[0].keys():
        >>>                vectors = [self.get_field(field_vector, document) for document in documents['documents']]
        >>>            else:
        >>>                vectors = [self.get_field(field_vector, document) for document in documents]
        >>>            
        >>>            X = np.stack(vectors)
        >>>            X_scaled = self.scaler.fit_transform(X)
        >>>            return self.model.fit_transform(X_scaled)
        >>>    
        >>>        def transform(self, X):
        >>>            if isinstance(documents[0], dict):
        >>>                if 'documents' in documents[0].keys():
        >>>                    vectors = [document[field_vector] for document in documents['documents']]
        >>>                else:
        >>>                    vectors = [document[field_vector] for document in documents]
        >>>            X_scaled = self.scaler.transform(vectors)
        >>>            return self.model.transform(X_scaled)
    """
    
    def fit_transform(self, documents: list, vector_field: str):
        """
        Fit and transform

        Args:
            documents:
                A list of lists to flatten to make into 1 list.
            vector_field:
                The vector field to fit and transform
        Returns:
            A dimensionality reduced array:
                A numpy array with less dimensions than the original.

        Example:

        >>> class IVISDimensionalityReduction(ViDimensionalityReductionBase):
        >>>     def __init__(self, batch_size=120, k=15, embedding_dims=2):
        >>>         self.scaler = MinMaxScaler()
        >>>         self.model = Ivis(embedding_dims=embedding_dims, k=k, batch_size=batch_size)
        >>>     def fit_transform(self, documents, field_vector):
        >>>           if isinstance(documents[0], dict):
        >>>             if 'documents' in documents[0].keys():
        >>>                vectors = [self.get_field(field_vector, document) for document in documents['documents']]
        >>>            else:
        >>>                vectors = [self.get_field(field_vector, document) for document in documents]
        >>>            
        >>>            X = np.stack(vectors)
        >>>            X_scaled = self.scaler.fit_transform(X)
        >>>            return self.model.fit_transform(X_scaled)
        >>>    
        >>>        def transform(self, X):
        >>>            if isinstance(documents[0], dict):
        >>>                if 'documents' in documents[0].keys():
        >>>                    vectors = [document[field_vector] for document in documents['documents']]
        >>>                else:
        >>>                    vectors = [document[field_vector] for document in documents]
        >>>            X_scaled = self.scaler.transform(vectors)
        >>>            return self.model.transform(X_scaled)
        """
        pass
    
    def transform(self, documents: List[Dict[str, Any]]):
        """
        Transform documents

        Args:
            documents:
                A list of lists to flatten to make into 1 list.
        
        Returns:
            transformed array:
                A transformed numpy array

        Example:
        
        >>> class IVISDimensionalityReduction(ViDimensionalityReductionBase):
        >>>     def __init__(self, batch_size=120, k=15, embedding_dims=2):
        >>>         self.scaler = MinMaxScaler()
        >>>         self.model = Ivis(embedding_dims=embedding_dims, k=k, batch_size=batch_size)
        >>>     def fit_transform(self, documents, field_vector):
        >>>           if isinstance(documents[0], dict):
        >>>             if 'documents' in documents[0].keys():
        >>>                vectors = [self.get_field(field_vector, document) for document in documents['documents']]
        >>>            else:
        >>>                vectors = [self.get_field(field_vector, document) for document in documents]
        >>>            
        >>>            X = np.stack(vectors)
        >>>            X_scaled = self.scaler.fit_transform(X)
        >>>            return self.model.fit_transform(X_scaled)
        >>>    
        >>>        def transform(self, X):
        >>>            if isinstance(documents[0], dict):
        >>>                if 'documents' in documents[0].keys():
        >>>                    vectors = [document[field_vector] for document in documents['documents']]
        >>>                else:
        >>>                    vectors = [document[field_vector] for document in documents]
        >>>            X_scaled = self.scaler.transform(vectors)
        >>>            return self.model.transform(X_scaled)
        """
        pass
