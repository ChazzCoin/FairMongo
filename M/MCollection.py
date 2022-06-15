import time
from M import MDB, MServers
from FSON import DICT
from FList import LIST
from M.MCore import MCore
from FLog.LOGGER import Log
Log = Log("MCollection")

"""
    -> BASE CLASS
        - Collection Instance Object on top of MCore.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCollection(MCore):
    mcollection_name: str = None
    mcollection = None

    @classmethod
    def GET_SOZIN(cls):
        nc = cls()
        nc.SozinRemote()
        return nc

    @classmethod
    def construct_fig_host_collection(cls, hostName, collectionName, databaseName=False):
        nc = cls()
        if databaseName:
            # -> if provided database name
            nc.construct_fig_host_database(hostName, databaseName=databaseName)
        else:
            # -> Use Default Database.
            nc.construct_fig_host_database(hostName, databaseName=MServers.db_name)
        # -> if provided collection -> forcing it though
        if collectionName:
            nc.construct_mcollection(collectionName)
        return nc

    @classmethod
    def construct_manual_collection(cls, collectionName, hostName=MServers.db_environment_name, databaseName=MServers.db_name):
        nc = cls()
        if databaseName:
            # -> if provided database name
            nc.construct_fig_host_database(hostName, databaseName=databaseName)
        else:
            # -> Use Default Database.
            nc.construct_fig_host_database(hostName, databaseName=MServers.db_name)
        # -> if provided collection -> forcing it though
        if collectionName:
            nc.construct_mcollection(collectionName)
        return nc

    def construct_mcollection(self, collection_or_name):
        self.mcollection_name = str(collection_or_name)
        if not self.mcollection:
            self.mcollection = MDB.GET_COLLECTION(collection_or_name)

    def is_valid(self) -> bool:
        if not self.is_connected():
            return False
        if not self.mcollection:
            return False
        if not self.core_db.validate_collection(self.mcollection):
            return False
        return True

    @staticmethod
    def get_arg(key, value, default=False):
        return DICT.get(key, value, default=default)

    def get_document_count(self):
        return self.mcollection.estimated_document_count()

    def base_query(self, kwargs, page=0, limit=100):
        if not self.mcollection:
            return False
        if limit and page >= 0:
            results = self.mcollection.find(kwargs).skip(page).limit(limit)
        else:
            results = self.mcollection.find(kwargs)
        results = MCore.to_list(results)
        if results and len(results) > 0:
            return results
        return False

    def base_query_unlimited(self, kwargs):
        if not self.mcollection:
            return False
        results = self.mcollection.find(kwargs)
        results = MCore.to_list(results)
        if results and len(results) > 0:
            return results
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
            self.mcollection.insert_one(kwargs)
            Log.s(f"NEW Record created in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def update_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            time.sleep(1)
            self.mcollection.update_one( findQuery, updateQuery, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def replace_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            time.sleep(1)
            self.mcollection.replace_one( findQuery, updateQuery, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def update_many_records(self, findQuery: dict, updateQueries: list, upsert=True):
        try:
            time.sleep(1)
            self.mcollection.update_many( findQuery, updateQueries, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.mcollection_name} ]", error=e)
            return False

    def remove_record(self, kwargs):
        try:
            time.sleep(1)
            self.mcollection.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.mcollection_name} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.mcollection_name} ]", error=e)
            return False


if __name__ == '__main__':
    n = MCollection.construct_manual_collection("crypto_tickers")
    n.add_records({"date": "Today", "BTC": 26.76})
    # temp = n.get_document_count()
    # print(temp)