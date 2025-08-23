
from .document_reader import FirebaseReadClient

class FirebaseAddClient(FirebaseReadClient):

    def __init__(self):
        super().__init__()

    def add_document(self, collection_name:str, document:dict, id:str):
        collection_ref = self.database.collection(collection_name)

        collection_ref.document(id).set(document)
    
    def add_indexed_document(self, collection_name:str, document:dict):
        collection_ref = self.database.collection(collection_name)

        link = document["overview"]["link"].replace("/", "\\")
        print(link)
        documents = self.read_documents(collection_name)
        documents_with_link = [doc for doc in documents if link in doc]
        
        if not documents_with_link:
            next_index = 0
        else:
            indexes = [int(doc[-1]) for doc in documents_with_link]
            next_index = max(indexes) + 1

        collection_ref.document(f"{link}-{next_index}").set(document)