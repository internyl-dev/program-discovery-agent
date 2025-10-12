
import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

class FirebaseClient:

    def __init__(self):
        cred = credentials.Certificate(os.environ.get("FIREBASE_SDK_PATH"))
        firebase_admin.initialize_app(cred)

        self.database = firestore.client()

    def read_documents(self, collection_name:str):
        collection_ref = self.database.collection(collection_name)
        documents = collection_ref.stream()

        return {document.id: document.to_dict() for document in documents}

    def read_document(self, collection_name:str, document_id:str):
        collection_ref = self.database.collection(collection_name)
        document_ref = collection_ref.document(document_id)
        snapshot = document_ref.get()

        return snapshot.to_dict()

    def delete_document(self, collection_name:str, document_id:str):
        collection_ref = self.database.collection(collection_name)
        document_ref = collection_ref.document(document_id)

        document_ref.delete()

    def add_document(self, collection_name:str, document:dict, id:str):
        collection_ref = self.database.collection(collection_name)

        collection_ref.document(id).set(document)
    
    def add_indexed_document(self, collection_name:str, document:dict):
        collection_ref = self.database.collection(collection_name)

        link = document["overview"]["link"].replace("/", "\\")
        print(link)
        documents = self.read_client.read_documents(collection_name)
        documents_with_link = [doc for doc in documents if link in doc]
        
        if not documents_with_link:
            next_index = 0
        else:
            indexes = [int(doc[-1]) for doc in documents_with_link]
            next_index = max(indexes) + 1

        collection_ref.document(f"{link}-{next_index}").set(document)