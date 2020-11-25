import time
import pytest

class TestCompare:
    @pytest.mark.use_client
    def test_setup(self, test_client, test_collection_name):
        """
            Test Setup.
        """
        num_of_docs = 50
        if test_collection_name in test_client.list_collections():
            test_client.delete_collection(test_collection_name)
        documents = test_client.create_sample_documents(num_of_docs)
        test_client.set_field_across_documents('color_vector_',
        [test_client.generate_vector(50, num_of_constant_values=49) for x in range(num_of_docs)], documents)
        test_client.set_field_across_documents('color_2_vector_',
        [test_client.generate_vector(50, num_of_constant_values=49) for x in range(num_of_docs)], documents)
        results = test_client.insert_documents(test_collection_name, documents)
        time.sleep(10)
        assert results['inserted_successfully'] == num_of_docs
    
    @pytest.mark.use_client
    @pytest.mark.parametrize("test_vector_fields", [("color_vector_"), ("color_2_vector_")])
    def test_compare_tables_simple(self, test_client, test_collection_name, test_vector_fields):
        """
            Test compare a simple table.
        """
        time.sleep(10)
        id_document = test_client.random_documents(test_collection_name, 1)['documents'][0]
        print(id_document)
        df = test_client.compare_vector_search_results(test_collection_name,
        vector_fields=[test_vector_fields], id_document=id_document, label='color')
        assert df.shape[0] > 0

    @pytest.mark.use_client
    def test_compare_tables_2_columns(self, test_client, test_collection_name):
        """
            Test compare a simple table.
        """
        id_document = test_client.random_documents(test_collection_name, 1)['documents'][0]
        df = test_client.compare_vector_search_results(test_collection_name,
        vector_fields=["color_vector_", "color_2_vector_"], id_document=id_document, label='color')
        assert df.shape[0] > 0
        assert df.shape[1] == 2
    @pytest.mark.use_client
    def test_teardown(self, test_client, test_collection_name):
        """
            Teardown.
        """
        test_client.delete_collection(test_collection_name)
        time.sleep(5)
        assert test_collection_name not in test_client.list_collections()
