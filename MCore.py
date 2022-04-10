from pymongo import MongoClient
from pymongo.database import Database
from Futils import DICT, DATE
import fig
from dateutil import parser
from Futils.rsLogger.CoreLogger import Log
import datetime

from MQuery import QBuilder

s = " "
DEFAULT_SERVER_ENVIRONMENT = fig.get_server_environment_uri()
DEFAULT_DATABASE_NAME = fig.db_name
Log = Log(f"MCore")

"""
    -> THE MASTER BASE CLASS
        - The Database Instance Itself.
    -> Does not need a collection to be initiated.
    -> Other Classes inherent this object.
"""

class MCore(QBuilder):
    core_connection_status = False
    core_client: MongoClient
    core_db: Database
    core_collection: Database = False

    def construct_fig_host_database(self, hostName, databaseName=DEFAULT_DATABASE_NAME):
        Log.className = f"MCore HOST=[ {hostName} ], DATABASE=[ {databaseName} ]"
        Log.i(f"Initiating MongoDB with Fig Host: {hostName}")
        fig_host_uri = fig.get_server_environment_uri_for_host_name(hostName)
        if fig_host_uri:
            try:
                self.core_client = MongoClient(fig_host_uri)
                self.is_connected()
            except Exception as e:
                Log.e(f"Unable to initiate MongoDB: HOST=[ {fig.db_environment_name} ]", error=e)
                return False
            if databaseName:
                self.core_db = self.core_client.get_database(databaseName)
            return self
        return False

    def constructor(self, url=DEFAULT_SERVER_ENVIRONMENT, databaseName=DEFAULT_DATABASE_NAME):
        Log.className = f"MCore HOST=[ {fig.db_environment_name} ], DATABASE=[ {databaseName} ]"
        Log.i(f"Initiating MongoDB: URI={url}")
        try:
            self.core_client = MongoClient(url)
            self.is_connected()
        except Exception as e:
            Log.e(f"Unable to initiate MongoDB: URI={url}", error=e)
            return False
        self.core_db = self.core_client.get_database(databaseName)
        return self

    def is_connected(self) -> bool:
        try:
            info = self.core_client.server_info()
            if info:
                Log.d("MongoDB is Up.")
                self.core_connection_status = True
                return True
        except Exception as e:
            Log.e("MongoDB is Down.", error=e)
            self.core_connection_status = False
            return False
        return False

    def core_query(self, kwargs, page=0, limit=100):
        if not self.core_collection:
            return False
        if limit:
            results = self.core_collection.find(kwargs).skip(page).limit(limit)
        else:
            results = self.core_collection.find(kwargs)
        results = MCore.to_list(results)
        if results and len(results) > 0:
            return results
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
    def Hark(cls):
        nc = cls().constructor(fig.hark_mongo_db_uri)
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
        self.core_collection = self.core_db.get_collection(collection_name)
        return self.core_collection

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
    def get_now_date():
        return DATE.mongo_date_today()

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
