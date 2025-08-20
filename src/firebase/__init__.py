
from .documents_add import FirebaseAddClient
from .documents_delete import FirebaseDeleteClient

class FirebaseClient(FirebaseAddClient, FirebaseDeleteClient):
    
    def __init__(self):
        super().__init__()