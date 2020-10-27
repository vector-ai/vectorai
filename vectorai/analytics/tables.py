"""
The Table Mixin 
"""
import pandas as pd
from typing import List
from ..utils import get_random_int
from ..errors import APIError

class TableMixin:
    """
        Mixin For Tables For Easy Vector Comparison.
    """
    def _return_vector_search_results(self, collection_name: str, vector_field: str, id_value: str, label: str, 
    num_rows: int=10):
        """
            Return the results from a Pandas DataFrame
            vector_field: the vector field to compare with 
            id_value: the id value of the document 
            label: label to compare with 
            collection_name: collection name
            num_rows: The number of rows
        """
        results = self.advanced_search_by_id(collection_name, document_id=id_value, 
                                fields={vector_field:1}, page_size=num_rows)
        if 'results' not in results.keys():
            raise APIError(results)
        values = self.get_field_across_documents(label, results['results'])
        return values

    def compare_vector_search_results(self, collection_name: str, vector_fields: List[str], label: str,
    id_document: str=None, id_value: str=None, num_rows=10):
        """
            Compare vector results
            Args:
                vector_fields: The list of vectors
                id_value: The value of the ID of the document
                id_document: The document with the id_value in it
                label: The label for the vector
                num_rows: The number of rows to compare search results for
            Example:
                compare_vector_search_results(collection_name, vector_fields)
        """
        if id_value is None:
            print("Using a random document unless the id_value is specified.")
            id_document = self.random_documents(collection_name, page_size=1, seed=get_random_int())['documents'][0]
        if isinstance(id_document, dict):
            id_value = id_document['_id']
        values = {}
        for f in vector_fields:
            values[f] = self._return_vector_search_results(collection_name=collection_name, vector_field=f, 
        id_value=id_value, label=label, num_rows=num_rows)
        return pd.DataFrame.from_dict(values)
