
from .document_uploader import FirebaseAddClient
from .document_remover import FirebaseDeleteClient
class FirebaseClient(FirebaseAddClient, FirebaseDeleteClient):
    
    def __init__(self):
        super().__init__()

    def move_duplicates(self, collection1:str, collection2:str):
        docs = self.read_documents(collection1)

        urls = list(docs.keys())
        i=0
        while i < len(urls):
            doc = urls[i]

            common_url = doc[:-2]
            common_docs = [doc for doc in docs if doc[:-2] == common_url]
            max_index = max([doc[-1] for doc in common_docs])
            to_delete = [doc for doc in common_docs if doc[-1] != max_index]

            for id in to_delete:
                self.add_document(collection2, docs[id], id)
                self.delete_document(collection1, id)

            i+=1


if __name__ == "__main__":

    firebase = FirebaseClient()
    
    collection_to_add = "demo"
    collection_to_read = "internships-history"
    collection_history = "demo-history"

    documents = firebase.read_documents(collection_to_read)
    document = list(documents.values())[0]

    #firebase.add_indexed_document(collection_to_add, document)
    firebase.move_duplicates("demo", "demo-history")
    