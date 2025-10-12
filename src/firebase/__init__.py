
from .firebase_client import FirebaseClient

firebase = FirebaseClient()

if __name__ == "__main__":

    firebase = FirebaseClient()
    
    collection_to_add = "demo"
    collection_to_read = "internships-history"
    collection_history = "demo-history"

    documents = firebase.read_documents(collection_to_read)
    document = list(documents.values())[0]

    #firebase.add_indexed_document(collection_to_add, document)
    firebase.move_duplicates("demo", "demo-history")
    