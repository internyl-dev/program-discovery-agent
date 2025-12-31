
import os
from dotenv import load_dotenv
from typing import Optional, Self

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

load_dotenv()

class FirebaseClient:
    __shared_instance:Optional[Self] = None

    def __init__(self) -> None:

        if FirebaseClient.__shared_instance:
            raise Exception("Shared instance already exists")

        # Replace with the actual path
        cred = credentials.Certificate(os.environ.get("FIREBASE_SDK_PATH"))
        firebase_admin.initialize_app(cred)

        # Get a Firestore client
        self.database = firestore.client()

        FirebaseClient.__shared_instance = self

        #self.logger.debug("Firebase Admin SDK initialized and Firestore client ready!")

    @classmethod
    def get_instance(cls) -> Self:
        if not cls.__shared_instance:
            cls()
        assert cls.__shared_instance
        return cls.__shared_instance

    @staticmethod
    def _all_data_guard(collection_path: str, all_data: Optional[dict[str, dict]] = None) -> None:
        if (collection_path=="") and (all_data is None):
            raise ValueError("Either `collection_path` or `all_data` must be given, both empty")

    def save(self, 
             collection_path: str, 
             document: dict, 
             doc_id: Optional[str] = None) -> None:
        """
        
        """
        collection_ref = self.database.collection(collection_path)

        if doc_id:
            collection_ref.document(doc_id).set(document)
        else:
            update_item, doc_ref = collection_ref.add(document)

    def get_by_id(self, collection_path: str, doc_id: str) -> dict:
        "Returns just the data of the given ID"
        collection_ref = self.database.collection(collection_path)
        doc = collection_ref.document(doc_id).get()
        data = doc.to_dict()
        if data is not None:
            return data
        else:
            raise ValueError(f"Data of id '{doc_id}' not found")

    def get_all_data(self, collection_path: str)-> dict:
        ""
        collection_ref = self.database.collection(collection_path)
        documents = collection_ref.stream()

        return {document.id: document.to_dict() for document in documents}

    def delete_by_id(self, collection_path: str, doc_id: str) -> None:
        ""
        collection_ref = self.database.collection(collection_path)
        collection_ref.document(doc_id).delete()

    @staticmethod
    def get_link_from_id(doc_id: str) -> str:
        ""
        return "-".join(doc_id.split("-")[:-1])
    
    @staticmethod
    def get_version_from_id(doc_id: str) -> int:
        ""
        return int(doc_id.split("-")[-1])

    def link_in_id(self, doc_id: str, link: str) -> bool:
        ""
        return self.get_link_from_id(doc_id) == link

    def get_latest_entry(self,  
                         link: str, 
                         collection_path: str = "",
                         all_data: Optional[dict[str, dict]] = None) -> dict[str, dict]:
        """
        Gets the latest data entry of the specified link
        Returns:
            {id (str): data (dict)}
        """
        self._all_data_guard(collection_path, all_data)

        all_data = all_data or self.get_all_data(collection_path)

        # Documents end with a "-" followed by a number representing the version of the doc
        # Find all data with the same link as the link provided
        docs_with_link: dict[int, dict] = {}
        for doc_id in all_data:
            if self.link_in_id(doc_id, link):
                # {version: {id: data}}
                ver = self.get_version_from_id(doc_id)
                docs_with_link[ver] = {doc_id: all_data[doc_id]}

        if not docs_with_link:
            raise LookupError(f"No documents with link '{link}' found")

        max_ver: int = max(docs_with_link.keys())
        return docs_with_link[max_ver]

    def get_all_latest_entries(self, 
                               collection_path: str = "", 
                               all_data: Optional[dict[str, dict]] = None) -> dict[str, dict]:
        """
        Returns all latest data entries
        Returns:
            {id (str): data (dict)}
        """
        self._all_data_guard(collection_path, all_data)

        all_data = all_data or self.get_all_data(collection_path)

        all_latest_entries: dict[str, dict] = {}
        for doc_id in all_data:
            if doc_id not in all_latest_entries:
                all_latest_entries.update(self.get_latest_entry(self.get_link_from_id(doc_id), 
                                          collection_path, 
                                          all_data))
        
        return all_latest_entries

    def get_all_old_entries(self, 
                            collection_path: str = "", 
                            all_data: Optional[dict[str, dict]] = None) -> dict[str, dict]:
        """
        
        """
        self._all_data_guard(collection_path, all_data)
        
        all_data = all_data or self.get_all_data(collection_path)
        all_latest_entries = self.get_all_latest_entries(all_data=all_data)

        return {doc_id: all_data[doc_id] for doc_id in all_data if doc_id not in all_latest_entries}