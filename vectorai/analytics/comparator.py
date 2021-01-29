from typing import List, Dict, Optional
from ..read import ViReadClient
from ..client import ViClient
from .api.comparator import ComparatorAPI

class ComparatorClient(ComparatorAPI, ViClient):
    def __init__(self, username: str=None, api_key: str=None, 
    url: str = "https://api.vctr.ai", 
    analytics_url="https://vector-analytics.vctr.ai"):
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
                return HTML(content.decode())
            return content
        self.write_to_html(content)
        print(f"Written to {html_file}.")
        return content

    def compare_ranks(
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
        colors: List[str]=['#ccff99', 'powderblue', '#ffc2b3'],
        html_file: str=None
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
        content = self._compare_ranks(ranked_list_1, ranked_list_2, 
            column_titles=column_titles, fields_to_display=fields_to_display,
            image_fields=image_fields, audio_fields=audio_fields,
            x_axis_title=x_axis_title, y_axis_title=y_axis_title,
            header=header, subheader=subheader, colors=colors)
        return self.output(content)

    def compare_search(
        self,
        collection_name: str,
        vector_fields: List[str],
        vector : List[float],
        fields_to_display: List[str]=None,
        image_fields: List[str]=[],
        audio_fields: List[str]=[],
        x_axis_title: str = 'Fields',
        y_axis_title: str = 'Vector fields',
        header: str = "<h1>Top-K Ranking Comparator</h1>",
        subheader: str = "<h2>Compare ranks in the different lists.</h2>",
        colors: List[str]=['#ccff99', 'powderblue', '#ffc2b3']
    ):  
        """
        Compare Searching By ID
        """
        ranked_list_1 = self.search(
            collection_name,
            vector=vector,
            field=vector_fields[0])
        ranked_list_2 = self.search_by_id(
            collection_name, 
            vector=vector, 
            field=vector_fields[1])
        return self.compare_ranks(
            ranked_list_1,
            ranked_list_2,
            column_titles=vector_fields,
            fields_to_display=fields_to_display,
            image_fields=image_fields,
            audio_fields=audio_fields,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            header=header,
            subheader=subheader,
            colors=colors
        )
    
    def random_compare_search_by_id(
        self,
        collection_name: str,
        vector_fields: List[str],
        fields_to_display: List[str]=None,
        image_fields: List[str]=[],
        audio_fields: List[str]=[],
        x_axis_title: str = 'Fields',
        y_axis_title: str = 'Vector fields',
        header: str = "<h1>Top-K Ranking Comparator</h1>",
        subheader: str = "<h2>Compare ranks in the different lists.</h2>",
        colors: List[str]=['#ccff99', 'powderblue', '#ffc2b3'],
        page_size=15,
    ):
        fields_to_include = ['_id'] + vector_fields
        random_docs = self.random_documents(collection_name, page_size=1,
        include_fields=fields_to_include)['documents']
        random_id = random_docs[0]['_id']
        ranked_list_1 = self.search_by_id(
            collection_name, 
            random_id, 
            field=vector_fields[0],
            page_size=page_size)['results']
        ranked_list_2 = self.search_by_id(
            collection_name, 
            random_id, 
            field=vector_fields[1],
            page_size=page_size)['results']
        return self.compare_ranks(
            ranked_list_1,
            ranked_list_2,
            column_titles=vector_fields,
            fields_to_display=fields_to_display,
            image_fields=image_fields,
            audio_fields=audio_fields,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            header=header,
            subheader=subheader,
            colors=colors
        )

    def compare_search_by_id(
        self,
        collection_name: str,
        vector_fields: List[str],
        document_id: str,
        fields_to_display: List[str]=None,
        image_fields: List[str]=[],
        audio_fields: List[str]=[],
        x_axis_title: str = 'Fields',
        y_axis_title: str = 'Vector fields',
        header: str = "<h1>Top-K Ranking Comparator</h1>",
        subheader: str = "<h2>Compare ranks in the different lists.</h2>",
        colors: List[str]=['#ccff99', 'powderblue', '#ffc2b3']
    ):  
        """
        Compare Searching By ID
        """
        ranked_list_1 = self.search_by_id(
            collection_name, 
            document_id, 
            field=vector_fields[0])
        ranked_list_2 = self.search_by_id(
            collection_name, 
            document_id, 
            field=vector_fields[1])
        return self.compare_ranks(
            ranked_list_1,
            ranked_list_2,
            column_titles=vector_fields,
            fields_to_display=fields_to_display,
            image_fields=image_fields,
            audio_fields=audio_fields,
            x_axis_title=x_axis_title,
            y_axis_title=y_axis_title,
            header=header,
            subheader=subheader,
            colors=colors
        )
