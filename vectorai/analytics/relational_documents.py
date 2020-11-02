"""
    Utilities for relational documents.
"""
from ..models.deployed.base import ViDeployedModel
import numpy as np
from itertools import permutations
from typing import List, Dict

def vector_operation(vector_1: list, vector_2: list, operation: str='mean', axis: int=0):
    """
        Perform vector operation between 2 vectors.
        Args:
            vector_1: First vector
            vector_2: Second vector
            Operation: The operation that can be used (mean/minus/sum/min/max)
            Axis: Axis on which to perform the vector operation
        Example:
            >>> vector_operation(np.array([1, 2, 3]), np.array([2, 3, 4]))
    """
    vectors = [vector_1, vector_2]
    if operation == "mean":
        return np.mean(vectors, axis=axis).tolist()
    elif operation == 'minus':
        return np.subtract(vector_1, vector_2).tolist()
    elif operation == "sum":
        return np.sum(vectors, axis=axis).tolist()
    elif operation == "min":
        return np.min(vectors, axis=axis).tolist()
    elif operation == "max":
        return np.max(vectors, axis=axis).tolist()
    else:
        raise ValueError("Vector operation needs to be one of minus/mean/sum/min/max.")

def create_relational_document(doc_1: Dict, doc_2: Dict, vector_fields: List[str], label_field: str, operation="minus"):
    """
        Args:
            Operation: minus/sum
            Vector_fields: The name of the vector fields
            label: The entity of the vector
        Example:
            >>> from vectorai.utils import UtilsMixin
            >>> mixin_utils = UtilsMixin()
            >>> doc = mixin_utils.create_sample_document()
            >>> doc_2 = mixin_utils.create_sample_document()
            >>> create_relational_document(doc_1, doc_2, vector_fields=['color_vector_'], label_field='country')
    """
    # Create a new document
    new_doc = {}
    for vector in vector_fields:
        new_vector = vector_operation(doc_1[vector], doc_2[vector], operation=operation)
        if operation.lower() == 'minus':
            new_label = doc_1[label_field] + " - " + doc_2[label_field]
        elif operation.lower() == 'sum':
            new_label = doc_1[label_field] + " + " + doc_2[label_field]
        elif operation.lower() == 'mean':
            new_label = "avg(" + doc_1[label_field] + ", " + doc_2[label_field] + ")"
        elif operation.lower() == 'max': 
            new_label = "max(" + doc_1[label_field] + ", " + doc_2[label_field] + ")"
        elif operation.lower() == 'min':
            new_label = "min(" + doc_1[label_field] + ", " + doc_2[label_field] + ")"
        new_doc.update({label_field: new_label, vector : new_vector})
    new_doc.update({'doc_1': doc_1, 'doc_2': doc_2})
    return new_doc

def create_relational_collection(docs: list, label_field: str, vector_fields: List[str], operation: str='minus'):
    """
        Create relational collection that.
        It should return n*(n-1) documents (for every permutation of the documents.
        Args:
            docs: The documents
            label_field: The field of the labels
            vector_fields: The vector fields in the document 
            operation: Must be one of minus/mean/max/min/sum.
        Example:
            create_relational_collection(docs)
    """
    perm = list(permutations(docs, 2))
    print("Returning n * (n - 1) documents. Insert and search to explore what relationships you end up with!")
    return [create_relational_document(*c, vector_fields=vector_fields, operation=operation, label_field=label_field) for i, c in enumerate(perm)]
