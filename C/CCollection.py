import time
from pymongo.database import Database
from FList import LIST
from FLog.LOGGER import Log
Log = Log("MCollection")

"""
    -> BASE CLASS
        - Collection Instance Object on top of MCore.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class CCollection:
    cn: str = None
    cc: Database = None

    def construct_cc(self, collection):
        self.cn = str(collection)
        self.cc = collection

    def get_document_count(self):
        return self.cc.estimated_document_count()

    def base_query(self, kwargs, page=0, limit=100):
        if not self.cc:
            return False
        if limit and page:
            results = self.cc.find(kwargs).skip(page).limit(limit)
        else:
            results = self.cc.find(kwargs)
        results = list(results)
        if results and len(results) > 0:
            return results
        return False

    def get_field_names(self):
        singleRecord = self.cc.find({}).limit(1)
        for item in singleRecord:
            return list(item.keys())
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
            self.cc.insert_one(kwargs)
            Log.s(f"NEW Record created in DB=[ {self.cn} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.cn} ]", error=e)
            return False

    def update_record(self, findQuery: dict, updateQuery: dict, upsert=True):
        try:
            time.sleep(1)
            self.cc.update_one( findQuery, updateQuery, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.cn} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.cn} ]", error=e)
            return False

    def update_many_records(self, findQuery: dict, updateQueries: list, upsert=True):
        try:
            time.sleep(1)
            self.cc.update_many( findQuery, updateQueries, upsert=upsert )
            Log.s(f"UPDATED Record in DB=[ {self.cn} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.cn} ]", error=e)
            return False

    def remove_record(self, kwargs):
        try:
            time.sleep(1)
            self.cc.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.cn} ]")
            return True
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.cn} ]", error=e)
            return False
