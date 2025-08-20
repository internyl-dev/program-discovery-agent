
from .document_uploader import FirebaseAddClient
from .document_remover import FirebaseDeleteClient

class FirebaseClient(FirebaseAddClient, FirebaseDeleteClient):
    
    def __init__(self):
        super().__init__()