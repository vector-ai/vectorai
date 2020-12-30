import time
from vectorai import ViClient, ViCollectionClient

class TempClient:
    def __init__(self, client, collection_name: str=None):
        self.client = client
        if isinstance(client, ViClient):
            self.collection_name = collection_name
        elif isinstance(client, ViCollectionClient):
            self.collection_name = self.client.collection_name
        
    def teardown_collection(self):
        if self.collection_name in self.client.list_collections():
            time.sleep(2)
            if isinstance(self.client, ViClient):
                self.client.delete_collection(self.collection_name)
            elif isinstance(self.client, ViCollectionClient):
                self.client.delete_collection()
    
    def __enter__(self):
        self.teardown_collection()
        return self.client
    
    def __exit__(self, *exc):
        self.teardown_collection()

class TempClientWithDocs(TempClient):
    """
        Temporary Client With Documents already inserted.
    """
    def __init__(self, client, collection_name: str=None, num_of_docs: int=10):
        self.client = client
        if isinstance(client, ViClient):
            self.collection_name = collection_name
        elif isinstance(client, ViCollectionClient):
            self.collection_name = self.client.collection_name
        self.num_of_docs = num_of_docs

    def __enter__(self):
        self.teardown_collection()
        self.client.insert_documents(self.collection_name, 
        self.client.create_sample_documents(self.num_of_docs))
        return self.client
