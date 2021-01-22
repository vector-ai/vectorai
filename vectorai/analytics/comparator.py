from typing import List, Dict
from ..utils import UtilsMixin
from ..read import ViReadClient
from ..write import ViWriteClient
from .api.comparator import ComparatorAPI

class ComparatorClient(ComparatorAPI, ViWriteClient, ViReadClient, UtilsMixin):
    def __init__(self, username: str=None, api_key: str=None, 
    url: str = "https://api.vctr.ai", analytics_url="https://vector-analytics.vctr.ai"):
        self.username = username
        self.api_key = api_key
        self.url = url
        self.analytics_url = analytics_url
    def write_to_html(self, content, file_name: str):
        with open(file_name, 'w') as f:
            f.write(content)
    
    def output(self, content, html_file: str=None):
        if html_file is None:
            if self.is_in_notebook():
                from IPython.display import HTML
                return HTML(content)
            return content
        self.write_to_html(content)
        print(f"Written to {html_file}.")
        return content

    def compare_topk(
        self, 
        results_list_1: List[Dict], 
        results_list_2: List[Dict], 
        vector_fields: List[str], 
        fields_to_display: List[str]=None,
        image_fields: List[str]=[], 
        audio_fields: List[str]=[],
        html_file: str=None
    ):
        """
        Compare Top-K Lists.
        Args:
            results_list_1: A list of results as a dictionary containing the required fields.
            results_list_2: Another list of results
            vector_fields: The vector field/s used to compare.
            fields_to_display: The fields required for displaying the object
            image_fields: The fields which are images 
            audio_fields: The fields which are audio
            html_file: the HTML file
        """
        content = self._compare_topk(results_list_1, results_list_2, 
            vector_fields=vector_fields, fields_to_display=fields_to_display,
            image_fields=image_fields, audio_fields=audio_fields)
        return self.output(content)

    def compare_topk_vectors(
        self, 
        results_list_1: List[Dict], 
        results_list_2: List[Dict], 
        vector_fields: List[str], 
        fields_to_display: List[str]=None,
        image_fields: List[str]=[], 
        audio_fields: List[str]=[],
        html_file: str=None
    ):
        """
        Compare Top-K Lists.
        Args:
            results_list_1: A list of results as a dictionary containing the required fields.
            results_list_2: Another list of results
            vector_fields: The vector field/s used to compare.
            fields_to_display: The fields required for displaying the object
            image_fields: The fields which are images 
            audio_fields: The fields which are audio
            html_file: the HTML file
        """
        content = self._compare_topk_vectors(
            results_list_1, results_list_2, 
            vector_fields=vector_fields, 
            fields_to_display=fields_to_display,
            image_fields=image_fields, 
            audio_fields=audio_fields)
        return self.output(content)

    def random_compare_topk_vectors(
        self,
        collection_name: str,
        vector_fields: List[str],
        fields_to_display: List[str]=None,
        image_fields: List[str]=None,
        audio_fields: List[str]=None,
        html_file: str=None
    ):
        assert len(vector_fields) == 2, ""
        random_document = self.random_documents(collection_name, page_size=1, include_fields=['_id'])['documents'][0]
        random_id = random_document['_id']
        results_1 = self.search_by_id(collection_name, random_id, field=vector_fields[0])['results']
        results_2 = self.search_by_id(collection_name, random_id, field=vector_fields[1])['results']
        return self.compare_topk_vectors(results_1, results_2, vector_fields=vector_fields,
        fields_to_display=fields_to_display, image_fields=image_fields, audio_fields=audio_fields, 
        html_file=html_file)

    
    def compare_topk_documents_by_ids(
        self, 
        collection_name: str,
        vector_field: str,
        document_ids: List[str],
        fields_to_display: List[str]=None,
        image_fields: List[str]=[], 
        audio_fields: List[str]=[],
        page_size: int=15
        ):
        """
        Compare Top-K Lists.
        Args:
            results_list_1: A list of results as a dictionary containing the required fields.
            results_list_2: Another list of results
            vector_fields: The vector field/s used to compare.
            fields_to_display: The fields required for displaying the object
            image_fields: The fields which are images 
            audio_fields: The fields which are audio
        """
        content = self._compare_topk_documents_by_ids(
            collection_name=collection_name, 
            vector_field=vector_field,
            document_ids=document_ids,
            fields_to_display=fields_to_display,
            image_fields=image_fields,
            audio_fields=audio_fields,
            page_size=page_size
        )
        return self.output(content)

    def random_compare_topk_documents_by_ids(
        collection_name: str,
        vector_field: str,
        fields_to_display: List[str]=[],
        image_fields: List[str]=[],
        audio_fields: List[str]=[],
        page_size: int=15,
        seed=None
    ):
        """Randomly compare Top K Documents by IDs
        """
        random_docs = self.random_documents(collection_name, 
        include_fields=['_id'] , page_size=2, seed=seed)['documents']
        random_ids = self.get_field_across_documents('_id', random_docs)
        return self.random_compare_topk_documents_by_ids(
            collection_name=collection_name, 
            vector_field=vector_field,
            document_ids=random_ids,
            fields_to_display=fields_to_display,
            image_fields=image_fields,
            audio_fields=audio_fields,
            page_size=page_size
        )
