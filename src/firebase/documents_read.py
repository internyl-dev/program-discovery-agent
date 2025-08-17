
import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

class FirebaseReadClient:

    def __init__(self):
        cred = credentials.Certificate(os.environ.get("FIREBASE_SDK_PATH"))
        firebase_admin.initialize_app(cred)

        self.database = firestore.client()

    def read_documents(self, collection_name:str):
        collection_ref = self.database.collection(collection_name)
        documents = collection_ref.stream()

        return [(document.to_dict()) for document in documents]

    def read_document(self, collection_name:str, document_id:str):
        collection_ref = self.database.collection(collection_name)
        document_ref = collection_ref.document(document_id)