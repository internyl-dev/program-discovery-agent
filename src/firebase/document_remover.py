
from .document_reader import FirebaseReadClient

class FirebaseDeleteClient(FirebaseReadClient):
    def __init__(self):
        super().__init__()

    def delete_document(self, collection_name:str, document_id:str):
        collection_ref = self.database.collection(collection_name)
        document_ref = collection_ref.document(document_id)

        document_ref.delete()