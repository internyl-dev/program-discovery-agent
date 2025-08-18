
from .documents_read import FirebaseReadClient

class FirebaseAddClient(FirebaseReadClient):

    def __init__(self):
        super().__init__(self)
    
    def add_document(self, collection_name:str, document:dict):
        collection_ref = self.database.collection(collection_name)
        collection_ref.add(document)