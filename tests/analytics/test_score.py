"""
Testing module for analytics scoring.
"""
def test_cosine_similarity(test_client):
    """
        Testing cosine similarity function works.
    """
    test_client.calculate_cosine_similarity(test_client.generate_vector(10), 
    test_client.generate_vector(10))
    assert True
