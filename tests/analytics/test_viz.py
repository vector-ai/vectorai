"""
    Test visualisations
"""
import plotly.graph_objects as go

def test_radar_plot_across_documents(test_client):
    """
        Test radar plots across documents
    """
    docs = test_client.create_sample_documents(5)
    fig = test_client.plot_radar_across_documents(docs, anchor_documents=docs[0:2], 
        vector_field='color_vector_', label_field='color')
    assert isinstance(fig, go.Figure)

def test_radar_plot_across_vector_fields(test_client):
    """
        Test radar plots across documents.
    """
    docs = test_client.create_sample_documents(5)
    fig = test_client.plot_radar_across_vector_fields(docs, anchor_document=docs[0], 
    vector_fields=['color_vector_', 'color_2_vector_'], label_field='country')
    assert isinstance(fig, go.Figure)
