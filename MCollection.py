import time

import fig
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

    @classmethod
    def construct_fig_host_collection(cls, hostName, collectionName, databaseName=False):
        nc = cls()
        if databaseName:
            # -> if provided database name
            nc.construct_fig_host_database(hostName, databaseName=databaseName)
        else:
            # -> Use Default Database.
            nc.construct_fig_host_database(hostName, databaseName=databaseName)
        # -> if provided collection -> forcing it though
        if collectionName:
            nc.private_set_collection(collectionName)
        return nc

    def private_set_collection(self, collection_or_name):
        self.collection_name = str(collection_or_name)
        self.collection = self.get_collection(collection_or_name)

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
        res = self.query({})
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


if __name__ == '__main__':
    n = MCollection
    n.construct_fig_host_collection(fig.HARK, "articles")
    n.init_FIND(n.collection_name)