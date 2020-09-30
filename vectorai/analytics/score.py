"""Scoring Functions to compare for analytics.
"""
from typing import Dict, Any, List
from ..read import ViReadClient
from numpy import inner
from numpy.linalg import norm

class ViScore(ViReadClient):
    @staticmethod
    def calculate_cosine_similarity(a, b):
        return inner(a, b) / (norm(a) * norm(b))
    
    def get_cosine_similarity_scores(
        self,
        other_documents: List[Dict[str, Any]],
        anchor_document: Dict[str, Any],
        vector_field: str,
    ) -> List[float]:
        """
        Compare scores based on cosine similarity

        Args:
            other_documents:
                List of documents (Python Dictionaries)
            anchor_document:
                Document to compare all the other documents with.
            vector_field:
                The field in the documents to compare
        
        Example:
            >>> documents = [{...}]
            >>> ViClient.get_cosine_similarity_scores(documents[1:10], documents[0])
        """
        similarity_scores = []
        for i, doc in enumerate(other_documents):
            similarity_score = self.calculate_cosine_similarity(
                self.get_field(vector_field, doc),
                self.get_field(vector_field, anchor_document)
            )
            similarity_scores.append(similarity_score)
        return similarity_scores
