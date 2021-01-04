"""
Plotting functions of Vi go here. 
"""
import plotly.express as px
import plotly.graph_objects as go
import copy
import random
from typing import Union, List, Dict, Any
from plotly.subplots import make_subplots
from tqdm.notebook import tqdm
from .score import ViScore
from .utils import ViAnalyticsUtils, MeanDict
from ..read import ViReadClient
from ..errors import APIError

class VizMixin(ViScore, ViAnalyticsUtils):
    """
    Visualisation submodule for the library.
    """
    def _scatter_plot_documents(
        self,
        filtered_collection: list,
        dim_reduction_field: str,
        color: str,
        point_label: str,
        title: str=None,
        mode: str='markers',
        marker_size:int = 5
    ):
        """
        Add additional plot to figure and filtered collection and dim reduction field.

        Args:
            filtered_collection:
                A collection or the name of a collection
            dim_reduction_field:
                Dimensionally reduced field.
            color:
                Color of the plot
            point_label:
                Label of the plot
            title:
                Name of the group of documents

        Returns:
            go.Scatter: Scatter plot of centroids.

        """
        return go.Scatter(
            x=[
                self.get_field(dim_reduction_field, x)[0]
                for x in filtered_collection
            ],
            y=[
                self.get_field(dim_reduction_field, x)[1]
                for x in filtered_collection
            ],
            mode=mode,
            marker=dict(size=marker_size, color=color),
            text=[x[point_label] for x in filtered_collection],
            name=title,
        )

    def _scatter_plot_centroids(
        self,
        cluster_centroid_documents: List[Dict],
        dim_reduction_field: str,
        point_label: str,
        line_color="DarkSlateGrey",
        line_width=2,
        size=5,
        color_dict=None,
        mode: str='markers',
        color='orange',
    ):
        """
        Scatterplot the centroids

        Args:
            cluster_centroid_documents:
                The centroids to highlight.
            point_label:
                The label of every point. This should be found in the document.
            dim_reduction_field:
                The dimensionally-reduced vectors.
            line_width:
                The width of the lines.
            line_color:
                THe line color of the centroids
            color_dict:
                What to color the centroid the cluster label/title
            size:
                The size of the markers for the centroid documents
        
        Returns:
            go.Scatter: Scatter plot of the documents
        
        """
        x = [
            self.get_field(dim_reduction_field, x)[0]
            for x in cluster_centroid_documents.values()
        ]
        y = [
            self.get_field(dim_reduction_field, x)[1]
            for x in cluster_centroid_documents.values()
        ]
        titles = [
            self.get_field(point_label, x)
            for x in cluster_centroid_documents.values()
        ]
        return go.Scatter(
            x=x,
            y=y,
            mode=mode,
            marker=dict(
                size=size,
                # color=[color_dict[str(x['_clusters_'][cluster_field]['title'])] for x in cluster_centroids.values()],
                color=color,
                line=dict(width=line_width, color=line_color),
            ),
            text=titles,
            name="centroids",
        )

    def plot_dimensionality_reduced_vectors(
        self,
        collection: Union[str, List[Dict]],
        point_label: str,
        dim_reduction_field: str,
        cluster_field: str=None,
        cluster_label: str=None,
        include_centroids: bool = False,
        color: str=None,
        alias: str = None,
        mode: str='markers',
    ):
        """
        Returns a 2D plot of vectors that have been dimensionally reduced.

        Args:
            collection:
                A collection or the name of a collection
            point_label:
                The label of every point. This should be found in the document.
            dim_reduction_field:
                The dimensionally-reduced vectors.
            cluster_field:
                The field by which it is clustered.
            cluster_label:
                The name of the clusters
            include_centroids:
                Whether to include the centroids of every cluster
        
        Returns:
            Plotly figure object
        
        See example from: https://colab.research.google.com/drive/10u7b3lkIVJ-lceCmr34ywscOGueIFd0I?usp=sharing
        
        Example:
            >>> collection_name = 'nlp-qa'
            >>> cluster_field = 'question_vector_'
            >>> cluster_label = 'category'
            >>> alias = '1st_cluster'
            >>> dim_reduction_field = '_dr_.default.2.question_vectors_' # the '.' in names implies nested dictionaries in Vi
            >>> vi_client.plot_dimensionality_reduced_vectors(collection=collection_name,
                    cluster_field=cluster_field,
                    cluster_label=cluster_label,
                    point_label='question_title',
                    dim_reduction_field=dim_reduction_field, 
                    include_centroids=True, 
                    alias=alias)
        
        """
        fig = go.Figure()
        if include_centroids:
            if not isinstance(collection, str):
                raise NotImplementedError(
                    "Centroid visualisation not included for custom clustering."
                    + "Please add them to yourself by using add_trace to the returned fig output."
                )

            cluster_centroid_documents = self.advanced_cluster_centroid_documents(
                collection, cluster_field, alias=alias
            )

            fig.add_trace(
                self._scatter_plot_centroids(
                    cluster_centroid_documents=cluster_centroid_documents,
                    dim_reduction_field=dim_reduction_field,
                    point_label=point_label,
                    mode=mode
                )
            )

        # If collection is simply a name, retrieve collection
        if isinstance(collection, str):
            fields_to_include = [point_label, dim_reduction_field, cluster_field, cluster_label]
            fields_to_include = [x for x in fields_to_include if x is not None]
            collection = self.retrieve_all_documents(collection, include_fields=[fields_to_include])

        if cluster_label is None:
            color_dict = None
        else:
            cluster_titles = [
                self.get_field(cluster_label, x) for x in collection
            ]
            cluster_titles = list(set(cluster_titles))
            cluster_titles_color_map = dict(enumerate(cluster_titles))
            color_dict = {v: k + 5 for k, v in cluster_titles_color_map.items()}
        
        if cluster_label is None:
            fig.add_trace(
                self._scatter_plot_documents(
                    filtered_collection=collection,
                    dim_reduction_field=dim_reduction_field,
                    color=color,
                    point_label=point_label,
                    mode=mode
                )
            )
        else:
            for title in tqdm(cluster_titles):
                filtered_collection = [
                    x
                    for x in collection
                    if self.get_field(cluster_label, x) == title
                ]
                fig.add_trace(
                    self._scatter_plot_documents(
                        title=title,
                        filtered_collection=filtered_collection,
                        dim_reduction_field=dim_reduction_field,
                        color=color_dict[title],
                        point_label=point_label,
                    )
                )
            fig.update_layout(showlegend=True)
        return fig

    def plot_1d_cosine_similarity(
        self,
        documents: list,
        vector_fields: List[str],
        label: str,
        anchor_document: dict = None,
        anchor_index: Union[str, int] = 0,
        orientation: int="h",
        barmode: int="group",
        num_cols: int=None,
        y_axis_tickangle: int=-15,
        x_axis_tickangle: int=15
    ):
        """
        Compare 1 document against other documents.
        Ensure that the name is unique, otherwise the plot will simply take the mean.
        
        Args:
            documents: list of documents (dictionaries) to feed in
            vector_fields: vector field to calculate cosine similarity on 
            label: the x label for the bar plot 
            anchor_document: the document to compare it on
            anchor_index: the anchor index to compare it on
            orientation: The orientation of the bar chart. Can be 'v' (vertical) or 'h' (horizontal)
            num_cols: The number of columns. The default will put everything into 1 row. If you want to 
            put things into multiple rows, then please reduce the number of columns. 
            y_axis_tickangle: This will change the tick angles of the y axis in the vertical chart.
            x_axis_tickangle: This will change the tick angels of the x axis in the vertical chart.
        Returns:
            Plotly Figure: returns a horizontal barplot showing cosine similarity scores.
        
        Example:
            >>> cluster_field = 'question_vector_'
            >>> cluster_label = 'category'
            >>> alias = '1st_cluster'
            >>> dim_reduction_field = '_dr_.default.2.question_vectors_' # the '.' in names implies nested dictionaries in Vi
            >>> vi_client.plot_1d_cosine_similarity(collection=collection_name,
                    cluster_field=cluster_field,
                    cluster_label=cluster_label,
                    point_label='question_title',
                    dim_reduction_field=dim_reduction_field, 
                    include_centroids=True, 
                    alias=alias)
        
        """
        if isinstance(vector_fields, str):
            vector_fields = [vector_fields]
        if anchor_document is None:
            other_documents = copy.deepcopy(documents)
            if isinstance(anchor_index, int):
                anchor_document = other_documents.pop(anchor_index)
            elif isinstance(anchor_index, str):
                # Loop through list to get ID
                for i, doc in enumerate(other_documents):
                    if anchor_index == doc["_id"]:
                        anchor_document = other_documents.pop(i)
                        break
        import math
        if num_cols is None:
            num_cols = len(vector_fields)
        fig = make_subplots(rows=int(len(vector_fields) / num_cols) + 1, cols=num_cols, 
        subplot_titles=vector_fields)
        row_num = 1
        col_num = 1
        for i, vector_field in enumerate(vector_fields):
            fig.add_trace(self._plot_1d_cosine_similarity_for_1_vector_field(
                documents=documents,
                vector_field=vector_field,
                label=label,
                anchor_document=anchor_document, 
                anchor_index=anchor_index,
                orientation=orientation),
                row=row_num, col=col_num)
            if col_num % num_cols == 0:
                row_num += 1
                col_num = 1
            else:
                col_num += 1
        if orientation == 'h':
            fig.update_yaxes(tickangle=y_axis_tickangle)
        if orientation == 'v':
            fig.update_xaxes(tickangle=x_axis_tickangle)
        
        return fig
    
    def _plot_1d_cosine_similarity_for_1_vector_field(self, 
        documents: list,
        vector_field: str,
        label: str,
        anchor_document: dict=None,
        anchor_index: Union[str, int]=0,
        orientation="h") -> go.Bar:
            """
            Compare 1 document against other documents.

            Args:
                documents: list of documents (dictionaries) to feed in
                vector_fields: vector field to calculate cosine similarity on 
                label: the x label for the bar plot 
                anchor_document: the document to compare it on
                anchor_index: the anchor index to compare it on
                orientation: The orientation of the bar chart
            Returns:
                None, returns a horizontal barplot showing cosine similarity scores.

            Example:
                >>> cluster_field = 'question_vector_'
                >>> cluster_label = 'category'
                >>> alias = '1st_cluster'
                >>> dim_reduction_field = '_dr_.default.2.question_vectors_' # the '.' in names implies nested dictionaries in Vi
                >>> vi_client.plot_1d_cosine_similarity(collection=collection_name,
                        cluster_field=cluster_field,
                        cluster_label=cluster_label,
                        point_label='question_title',
                        dim_reduction_field=dim_reduction_field, 
                        include_centroids=True, 
                        alias=alias)
            
            """
            
            try:
                scores = self.get_cosine_similarity_scores(
                    documents, anchor_document, vector_field=vector_field
                )
            except NameError:
                raise APIError(f"Anchor document with {anchor_index} not found.")

            for i, doc in enumerate(documents):
                doc["cos_score"] = scores[i]

            mean_dict = MeanDict()
            for i, doc in enumerate(documents):
                mean_dict[doc[label]] = doc["cos_score"]
            
            x, y = mean_dict.get_x_y()
            if orientation == 'h':
                return go.Bar(
                    x=y,
                    y=x,
                    orientation=orientation,
                    name=vector_field
                )
            else:
                return go.Bar(
                    x=x,
                    y=y,
                    text=x,
                    orientation=orientation,
                    name=vector_field
                )
        
    # def plot_2d_cosine_similarity(
    #     self,
    #     documents: List[Dict[str, Any]],
    #     anchor_documents: List[Dict[str, Any]],
    #     vector_fields: Union[str, List[str]],
    #     label: str,
    #     mode: str='markers+text'
    # ):
    #     """
    #     Plot cosine similarity with 2 anchor documents to compare with against other documents.

    #     Args:
    #         documents: list of documents (dictionaries) to feed in
    #         vector_field: vector field to calculate cosine similarity on 
    #         label: the x label for the bar plot 
    #         anchor_document: the document to compare it on
    #         anchor_index: the anchor index to compare it on
    #     Returns:
    #         A scatterplot showing cosine similarity scores with each axes being a specific document.
        
    #     Example:
    #         >>> cluster_field = 'question_vector_'
    #         >>> cluster_label = 'category'
    #         >>> alias = '1st_cluster'
    #         >>> dim_reduction_field = '_dr_.default.2.question_vectors_' # the '.' in names implies nested dictionaries in Vi
    #         >>> vi_client.plot_2d_cosine_similarity(documents=documents[2:],
    #                 anchor_documents=documents[:2],
    #                 vector_fields=vector_field,
    #                 label=label
    #                 )

    #     """
    #     assert (
    #         len(anchor_documents) == 2
    #     ), "You need 2 anchor documents for a 2d cosine similarity plot."
    #     fig = go.Figure()
    #     if isinstance(vector_fields, str):
    #         vector_fields = [vector_fields]
    #     for vector_field in vector_fields:
            
    #         scores_x = self.get_cosine_similarity_scores(
    #             documents, anchor_documents[0], vector_field
    #         )
    #         scores_y = self.get_cosine_similarity_scores(
    #             documents, anchor_documents[1], vector_field
    #         )

    #         for i, doc in enumerate(documents):
    #             doc["cos_score_x"] = scores_x[i]
    #             doc["cos_score_y"] = scores_y[i]

    #         x = [round(x["cos_score_x"], 3) for x in documents]
    #         y = [round(x["cos_score_y"], 3) for x in documents]
    #         labels = [x[label] for x in documents]
    #         fig.add_trace(go.Scatter(x=x, y=y, text=labels, mode=mode, name=vector_field))
    #     fig.update_xaxes(title_text=f"Comparing with {anchor_documents[0][label]}")
    #     fig.update_yaxes(title_text=f"Comparing with {anchor_documents[1][label]}")
    #     fig.update_layout(
    #         title_text=f"2D Cosine Similarity Comparison With {anchor_documents[0][label]} and {anchor_documents[1][label]}"
    #     )
    #     return fig

    def random_colour(self, num_of_colors) -> List:
        levels = range(32,256,32)
        return [tuple(random.choice(levels) for _ in range(3)) for _ in range(num_of_colors)]

    def plot_2d_cosine_similarity(self, 
        documents: List[Dict], anchor_documents: List[Dict], vector_fields: List[str], 
        label: str, mode='markers+text', textposition='top center', show_spikes=True,
        text_label_font_size: int=12, text_label_font_family = "Rockwell",
        text_label_bgcolor="white",
        marker_colors=['purple', 'aquamarine'], metric='cosine',
        plot_bgcolor="#e6e6fa", spikedash='dot', spikethickness=1.5
    ):
        """
        Plotting 2D cosine similarity plots 
        Args:
            documents: The documents to 
            anchor_documents: Documents by which to compare against
            vector_fields: The list of vectors to accept 
            Label: The document field to label
            Mode: Whether to include markers or text (view Plotly documentation for more information)
            textposition: where the text labels should be in relation to the marker
            show_spikes: show the spikes in comparison to the x and y labels
            text_label_font_family: The font of the text
            text_label_font_size: The font size of the text
            marker_colors: The color of the markers If the number of colors do not
            match then we it randomly generates.
            metric: The metric to use. Currently only supports cosine similarity
            plot_bgcolor: The background color of the plot
            spikethickness: The thickness of the spikes
            spikedash: Type of line the spikes should be.
        Example:
            >>> vi_client = ViClient()
            >>> collection_name = 'ecommerce'
            >>> docs = vi_client.random_documents(collection_name)['documents']
            >>> vi_client.plot_2d_cosine_similarity(docs, docs[0:2], 
            vector_fields=['use_vector_'], label='name')
        """
        if metric != 'cosine':
            raise NotImplementedError("Cosine similarity score is currently not implemented.")

        assert (
            len(anchor_documents) == 2
        ), "You need 2 anchor documents for a 2d cosine similarity plot."

        fig = go.FigureWidget()
        
        if len(vector_fields) > len(marker_colors):
            num_of_extra_fields = len(vector_fields) - len(marker_colors)
            marker_colors += self.random_colour(num_of_extra_fields)

        for vector_field_counter, vector_field in enumerate(vector_fields):
            scores_x = self.get_cosine_similarity_scores(
                documents, anchor_documents[0], vector_field
            )
            scores_y = self.get_cosine_similarity_scores(
                documents, anchor_documents[1], vector_field
            )

            for i, doc in enumerate(documents):
                doc["cos_score_x"] = scores_x[i]
                doc["cos_score_y"] = scores_y[i]
            x = [round(x["cos_score_x"], 3) for x in documents]
            y = [round(x["cos_score_y"], 3) for x in documents]
            labels = self.get_field_across_documents(label, documents)
            comparisons = [x_i > y[i] for i, x_i in enumerate(x)]
            text_comparisons = ["has <b>lower</b> cosine similarity with" if c == True 
            else "has <b>higher</b> cosine similarity with" for c in comparisons]
            fig.add_trace(go.Scatter(x=x, y=y, 
                text=labels,
                mode=mode, 
                name=vector_field,
                customdata=text_comparisons,
                hovertemplate = label +": <b>%{text}<extra></extra><br></b>" + \
                "%{customdata} <br>" + \
                "<b>" + anchor_documents[1][label] + "</b> (%{y})<br>" + \
                "compared to <br>" + \
                "<b>" + anchor_documents[0][label] + "</b> (%{x})</b>",
                marker=dict(
                    color=marker_colors[vector_field_counter],
                    size=5,
                    line=dict(width=0.5, color='DarkSlateGrey')
                )))

        self.add_labels_to_figure(fig, x_axis_label=f"Cosine Similarity With {anchor_documents[0][label]}",
        y_axis_label=f"Cosine Similarity WIth {anchor_documents[1][label]}",
        title_text=f"2D Cosine Similarity Comparison With {anchor_documents[0][label]} and {anchor_documents[1][label]}")

        fig.update_traces(textposition=textposition)

        fig.update_xaxes(showspikes=show_spikes, 
        spikedash=spikedash, spikethickness=spikethickness)
        fig.update_yaxes(showspikes=show_spikes, 
        spikedash=spikedash, spikethickness=spikethickness)
        
        fig.update_layout(plot_bgcolor=plot_bgcolor)
        fig.update_layout(
            hoverlabel=dict(
                bgcolor=text_label_bgcolor,
                font_size=text_label_font_size,
                font_family=text_label_font_family
            )
        )
        return fig
    
    def add_labels_to_figure(self, fig, title_text: str, x_axis_label: str, y_axis_label: str):
        fig.update_xaxes(title_text=x_axis_label)
        fig.update_yaxes(title_text=y_axis_label)
        fig.update_layout(title_text=title_text)

    def _plot_radar(self, scores: list, spokes: list, name: str, fill=None):
        """
            Args:
                Scores: The list of scores for cosine similarity
                spokes: The outside labels 
                name: The name of the plot
        """
        return go.Scatterpolar(
            # Get the cosine similarity scores here 
            r=scores + [scores[0]],
            theta=spokes + [spokes[0]],
            fill=fill,
            name=name,
        )

    def plot_radar_across_documents(self, docs: List[Dict], anchor_documents: List[Dict], vector_field: str, 
    label_field: str, range: List=[0, 1], fill: str=None, scoring_metric ='cosine'):
        """
            Radar plot for 1D cosine similarity across documents.
            Args:
                docs: A list of documents 
                anchor_document: The document to compare against
                vector_field: The vector vector field
                label_field: The field of the documents to get labels.
        """
        categories = self.get_field_across_documents(label_field, docs)
        fig = go.Figure()
        for anchor_document in anchor_documents:
            if scoring_metric == 'cosine':
                scores = self.get_cosine_similarity_scores(docs, anchor_document, vector_field=vector_field)
            else:
                scores = scoring_metric(docs, anchor_document, vector_field=vector_field)
            fig.add_trace(self._plot_radar(scores=scores, spokes=categories, name=vector_field, fill=fill))
        
        fig.update_layout(
            polar=dict(
            radialaxis=dict(
                visible=True,
                range=range
            )),
            showlegend=True
        )
        return fig

    def plot_radar_across_vector_fields(self, docs: List[Dict], anchor_document: Dict, 
    vector_fields: List[str], label_field: str, range=[0, 1], fill=None, scoring_metric='cosine'):
        """
            Radar plot for 1D cosine similarity across different vector spaces.
            Args:
                docs: A list of documents 
                anchor_document: The document to compare against
                vector_fields: the different vector fields
                label_field: The field of the documents to get labels.
        """
        categories = self.get_field_across_documents(label_field, docs)
        fig = go.Figure()
        for vector in vector_fields:
            if scoring_metric == 'cosine':
                scores = self.get_cosine_similarity_scores(docs, anchor_document, vector_field=vector)
            else:
                scores = scoring_metric(docs, anchor_document, vector_field=vector)
            
            fig.add_trace(self._plot_radar(scores=scores, spokes=categories, name=vector, fill=fill))

        fig.update_layout(
            polar=dict(
            radialaxis=dict(
                visible=True,
                range=range
            )),
            showlegend=True 
        )
        return fig
