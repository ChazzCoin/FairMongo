
from Futils.rsLogger import Log
# from MCollection import MCollection
from CLI import UserRequest, main
from MCollection import MCollection
import MDB

Log = Log("cCollection")

""" The Master in control of Mongo Collections """

COMMANDS = {"1. Query -> { key: value } based Query System!": ""}

# FIELDS_IN_COLLECTION = []

def handle_collection_command(user_in):
    pass

def print_list_of_collections():
    Log.cli(main.COLLECTION_NAMES)

def display_options():
    for opt in COMMANDS.keys():
        Log.cli(f"{opt}")

def main_loop(db):
    processing = True
    while processing:

        # display_options()
        # user_in = UserRequest.user_request(main.PYMONGO_INPUT("Collection"))
        init_cCollection(db)
        # handle_collection_command(user_in)


def init_cCollection(db):
    print_list_of_collections()
    potential_collection_name = UserRequest.user_request("Please pick a Collection to Open.")
    if potential_collection_name in main.COLLECTION_NAMES:
        db_collection = MDB.GET_MCOLLECTION(potential_collection_name)
        Log.cli(f"{potential_collection_name} is ready!")
        FIELDS_IN_COLLECTION = get_fields(db_collection)
        print(FIELDS_IN_COLLECTION)
        # print options here
        for com in COMMANDS.keys():
            Log.cli(com)
        uni = UserRequest.user_request(f"Next?")

def get_fields(collection):
    singleRecord = collection.find({}).limit(1)
    for item in singleRecord:
        return list(item.keys())

def query(collection: MCollection, query):
    Log.cli(f"Query = [ {query} ]")
    return collection.base_query(query)