import time
from Futils import DICT
from MCore import MCore
from MQuery import Find
from Futils.rsLogger.CoreLogger import Log
from pymongo.database import Database
Log = Log("MCollection")

"""
    -> BASE CLASS
        - Collection Instance Object on top of MCore.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCollection(MCore, Find):
    collection_name: str = None
    collection: Database = None

    @classmethod
    def GET_SOZIN(cls):
        nc = cls()
        nc.Sozin()
        return nc

    def query(self, kwargs, page=0, limit=100):
        return self.base_query(kwargs, page=page, limit=limit)

    def is_valid(self) -> bool:
        if not self.is_connected():
            return False
        if not self.collection:
            return False
        if not self.db.validate_collection(self.collection):
            return False
        return True

    @staticmethod
    def get_arg(key, value, default=False):
        return DICT.get(key, value, default=default)

    def get_document_count(self):
        res = self.collection.find({})
        if res:
            return len(list(res))
        return False

    def insert_record(self, kwargs):
        try:
            time.sleep(1)
            self.collection.insert_one(kwargs)
            Log.s(f"NEW Record created in DB=[ {self.collection_name} ]")
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.collection_name} ]", error=e)

    def update_record(self, findQuery, updateQuery, upsert=True):
        try:
            time.sleep(1)
            self.collection.update_one( findQuery, updateQuery, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.collection_name} ]")
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.collection_name} ]", error=e)

    def remove_record(self, kwargs):
        try:
            time.sleep(1)
            self.collection.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.collection_name} ]")
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.collection_name} ]", error=e)
