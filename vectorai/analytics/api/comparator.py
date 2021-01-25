import requests
from typing import List, Dict, Optional
from ...api.utils import retry, return_response

class ComparatorAPI:
    def __init__(self, username: str=None, api_key: str=None, 
    url: str = "https://api.vctr.ai", analytics_url="https://vector-analytics.vctr.ai"):
        self.username = username
        self.api_key = api_key
        self.url = url
        self.analytics_url = analytics_url

    @retry()
    def _compare_ranks(
        self, 
        ranked_list_1: List[Dict],
        ranked_list_2: List[Dict],
        fields_to_display: List[str]=None,
        image_fields: List[str]=[],
        audio_fields: List[str]=[],
        column_titles: Optional[List[str]] = None,
        x_axis_title: str = 'Fields',
        y_axis_title: str = 'Comparing: ',
        header: str = "<h1>Top-K Ranking Comparator</h1>",
        subheader: str = "<h2>Compare ranks in the different lists.</h2>",
        colors: List[str]=['#ccff99', 'powderblue', '#ffc2b3']
        ):
        """
        Compare Top-K Lists.
        Args:
            ranked_list_1: A list of results as a dictionary containing the required fields.
            ranked_list_2: Another list of results
            fields_to_display: The fields required for displaying the object
            image_fields: The fields which are images 
            audio_fields: The fields which are audio
            column_titles: The name of the columns for the differnt rank fields
            x_axis_title: The title of the x axis 
            y_axis_title: The title of the y axis
            header: The name of the graph 
            subheader: The sub-header of the graph
        """
        response = requests.post(
            url= f"{self.analytics_url}/comparator/compare_ranks/",
            json={
                "username": self.username,
                "api_key": self.api_key,
                "ranked_list_1": ranked_list_1,
                "ranked_list_2": ranked_list_2,
                "fields_to_display": fields_to_display,
                "image_fields": image_fields,
                "audio_fields": audio_fields,
                "column_titles": column_titles,
                "x_axis_title": x_axis_title,
                "y_axis_title": y_axis_title,
                "header": header,
                "subheader": subheader,
                "colors": colors,
            }
        )
        return return_response(response, return_type='content')
