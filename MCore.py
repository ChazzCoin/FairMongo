from pymongo import MongoClient
from pymongo.database import Database
from Futils import DICT, DATE
import fig
from dateutil import parser
from Futils.rsLogger.CoreLogger import Log
import datetime
Log = Log("MCore")

s = " "

SERVER_ENVIRONMENT = fig.get_server_environment_uri()
DEFAULT_DATABASE_NAME = fig.db_name

"""
    -> THE MASTER BASE CLASS
        - The Database Instance Itself.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCore:
    connection_status = False
    client: MongoClient
    db: Database

    def constructor(self, url=SERVER_ENVIRONMENT, databaseName=DEFAULT_DATABASE_NAME):
        Log.i(f"Initiating MongoDB at url={url}")
        try:
            self.client = MongoClient(url)
            self.is_connected()
        except Exception as e:
            Log.e("Unable to initiate MongoDB.", error=e)
            return False
        self.db = self.client.get_database(databaseName)
        return self

    def is_connected(self) -> bool:
        try:
            info = self.client.server_info()
            if info:
                Log.d("MongoDB is Up.")
                self.connection_status = True
                return True
        except Exception as e:
            Log.e("MongoDB is Down.", error=e)
            self.connection_status = False
            return False
        return False

    @classmethod
    def Sozin(cls):
        nc = cls().constructor(fig.sozin_mongo_db_uri)
        if nc.is_connected():
            return nc
        return False

    @classmethod
    def ArchivePi(cls):
        nc = cls().constructor(fig.archivepi_mongo_db_uri)
        if nc.is_connected():
            return nc
        return False

    @classmethod
    def Collection(cls, collection_name):
        nc = cls().constructor(fig.get_server_environment_uri())
        collect: Database = nc.get_collection(collection_name)
        return collect

    def get_collection(self, collection_name) -> Database:
        """
        INTERNAL/PRIVATE ONLY
        - DO NOT USE -
        """
        return self.db.get_collection(collection_name)

    """ OUT of database -> OFFICIAL DATE CONVERSION FROM DATABASE ENTRY <- """
    @staticmethod
    def from_db_date(str_date):
        date_obj = parser.parse(str_date)
        return date_obj

    """ INTO database -> OFFICIAL DATE CONVERSION FOR DATABASE ENTRY <- """
    @staticmethod
    def to_db_date(t=None):
        if t is None:
            t = datetime.datetime.now()
        date = str(t.strftime("%B")) + s + str(t.strftime("%d")) + s + str(t.strftime("%Y"))
        return date

    @staticmethod
    def parse_date(obj=None):
        if type(obj) is str:
            obj = DATE.parse_str(obj)
        elif type(obj) is list:
            return None
        p_date = str(obj.strftime("%B")) + s + str(obj.strftime("%d")) + s + str(obj.strftime("%Y"))
        return p_date

    @staticmethod
    def to_list(cursor):
        return list(cursor)

    @staticmethod
    def to_counted_dict(cursor):
        """ DEPRECATED """
        result_dict = {}
        for item in cursor:
            _id = DICT.get("_id", item)
            raw = DICT.get("raw_hookups", item)
            count = len(raw)
            result_dict[_id] = {"count": count,
                                "raw_hookups": raw}
        return result_dict

    @staticmethod
    def cursor_count(cursor) -> int:
        return len(list(cursor))
