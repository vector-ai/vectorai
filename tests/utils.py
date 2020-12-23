class TempClient:
    """
        Temporary client that will delete the collection if it fails.
    """
    def __init__(self, client, collection_name=None):
        self.client = client
        self.collection_name = collection_name

    def teardown_collection(self):
        if self.collection_name in self.client.list_collections():
            self.client.delete_collection(self.collection_name)
    
    def __enter__(self):
        self.teardown_collection()
        return self.client
    
    def __exit__(self, *exc):
        self.teardown_collection()

class TempClientWithDocs(TempClient):
    """
        Temporary client that will delete the collection if it fails.
        Automates the number of documents.
    """
    def __init__(self, client, collection_name=None, num_of_docs=10):
        self.client = client
        self.collection_name = collection_name
        self.num_of_docs = num_of_docs

    def __enter__(self):
        self.teardown_collection()
        self.client.insert_documents(self.collection_name, 
        self.client.create_sample_documents(self.num_of_docs))
        return self.client
