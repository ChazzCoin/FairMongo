import time

import MDB
import fig
from Futils import DICT, LIST
from MCore import MCore
from Futils.rsLogger.CoreLogger import Log
from pymongo.database import Database
Log = Log("MCollection")

"""
    -> BASE CLASS
        - Collection Instance Object on top of MCore.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCollection(MCore):
    collection_name: str = None
    collection = None

    @classmethod
    def GET_SOZIN(cls):
        nc = cls()
        nc.Sozin()
        return nc

    @classmethod
    def construct_fig_host_collection(cls, hostName, collectionName, databaseName=False):
        nc = cls()
        if databaseName:
            # -> if provided database name
            nc.construct_fig_host_database(hostName, databaseName=databaseName)
        else:
            # -> Use Default Database.
            nc.construct_fig_host_database(hostName, databaseName=fig.db_name)
        # -> if provided collection -> forcing it though
        if collectionName:
            nc.private_set_collection(collectionName)
        return nc

    def private_set_collection(self, collection_or_name):
        self.collection_name = str(collection_or_name)
        if not self.collection:
            self.collection = MDB.GET_COLLECTION(collection_or_name)

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

    def record_exists(self, recordIn) -> bool:
        temp = self.base_query(recordIn)
        if temp:
            Log.w("Object Exists in Database Already. Skipping...")
            return True
        Log.v("Object Does Not Exist in Database.")
        return False

    def add_records(self, list_of_objects):
        """ Each Object should be JSON Format """
        list_of_objects = LIST.flatten(list_of_objects)
        Log.w(f"Beginning Add Records Queue. COUNT=[ {len(list_of_objects)} ]")
        for objectItem in list_of_objects:
            article_exists = self.record_exists(objectItem)
            if not article_exists:
                self.insert_record(objectItem)
        Log.w(f"Finished Add Records Queue.")

    def insert_record(self, kwargs):
        try:
            time.sleep(1)
            self.collection.insert_one(kwargs)
            Log.s(f"NEW Record created in DB=[ {self.collection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.collection_name} ]", error=e)
            return False

    def update_record(self, findQuery, updateQuery, upsert=True):
        try:
            time.sleep(1)
            self.collection.update_one( findQuery, updateQuery, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.collection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.collection_name} ]", error=e)
            return False

    def remove_record(self, **kwargs):
        try:
            time.sleep(1)
            self.collection.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.collection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.collection_name} ]", error=e)
            return False


if __name__ == '__main__':
    n = MCollection
    n.construct_fig_host_collection(fig.HARK, "articles")
    n.init_FIND(n.collection_name)