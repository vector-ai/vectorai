from typing import List, Dict
from ...api.utils import retry, return_response

class ComparatorAPI:
    def __init__(self, username: str=None, api_key: str=None, 
    url: str = "https://api.vctr.ai", analytics_url="https://vector-analytics.vctr.ai"):
        self.username = username
        self.api_key = api_key
        self.analytics_url = url
        self.analytics_url = analytics_url

    @retry()
    def _compare_topk(
        self, 
        results_list_1: List[Dict], 
        results_list_2: List[Dict], 
        vector_fields: List[str]=[], 
        fields_to_display: List[str]=None,
        image_fields: List[str]=[], 
        audio_fields: List[str]=[]
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
        response = requests.post(
            url= f"{self.analytics_url}/comparator/compare_topk/",
            json={
                "username": self.username,
                "api_key": self.api_key,
                "results_list_1": results_list_1,
                "results_list_2": results_list_2,
                "vector_fields": vector_fields,
                "fields_to_display": fields_to_display,
                "image_fields": image_fields,
                "audio_fields": audio_fields
            }
        )
        return return_response(response, return_response='content')

    @retry()
    def _compare_topk_vectors(
        self, 
        results_list_1: List[Dict], 
        results_list_2: List[Dict], 
        vector_fields: List[str], 
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
        response = eequests.post(
            url= f"{self.analytics_url}/comparator/compare_topk_vectors/",
            json={
                "username": self.username,
                "api_key": self.api_key,
                "results_list_1": results_list_1,
                "results_list_2": results_list_2,
                "vector_fields": vector_fields,
                "fields_to_display": fields_to_display,
                "image_fields": image_fields,
                "audio_fields": audio_fields,
                "page_size": page_size
            }
        )
        return return_response(content, return_response='content')


    @retry()
    def _compare_topk_documents_by_ids(
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
        response = requests.post(
            url= f"{self.analytics_url}/comparator/compare_topk_documents_by_ids/",
            json={
                "username": self.username,
                "api_key": self.api_key,
                "results_list_1": results_list_1,
                "results_list_2": results_list_2,
                "vector_field": vector_field, 
                "fields_to_display": fields_to_display,
                "image_fields": image_fields, 
                "audio_fields": audio_fields,
                "page_size": page_size
            }
        )
        return return_response(response, return_response='content')
