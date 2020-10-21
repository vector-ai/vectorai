"""
The Table Mixin 
"""
import pandas as pd
from typing import List

class TableMixin:
    """
        Mixin For Tables For Easy Vector Comparison.
    """
    def _return_vector_search_results(self, collection_name: str, vector_field: str, id_value: str, label: str):
        """
            Return the results from a Pandas DataFrame
            vector_field: the vector field to compare with 
            id_value: the id value of the document 
            label: label to compare with 
            collection_name: collection name
        """
        results = self.advanced_search_by_id(collection_name=collection_name, 
        document_id=id_value, fields={vector_field: 1})['results']
        values = self.get_field_across_documents(label, results)
        return values

    def compare_vector_search_results(self, collection_name: str, vector_fields: List[str], label: str,
    id_document: str=None, id_value: str=None):
        """
            Compare vector results
            Args:
                vector_fields: The list of vectors
                id_value: The value of the ID of the document
                id_document: The document with the id_value in it
                label: The label for the vector
            Example:
                compare_vector_search_results(collection_name, vector_fields)
        """
        if isinstance(id_document, dict):
            id_value = id_document['_id']
        values = {}
        for f in vector_fields:
            values[f] = self._return_vector_search_results(collection_name, f, id_value, label)
        return pd.DataFrame.from_dict(values)
