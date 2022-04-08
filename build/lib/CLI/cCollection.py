from Futils import Regex
from Futils.rsLogger import Log, LogColors
# from MCollection import MCollection
from CLI import UserInput, SearchArticles, main
from MCollection import MCollection

Log = Log("cCollection")

COMMANDS = {"1. Query -> { key: value } based Query System!": ""}

def handle_collection_command(user_in):
    pass

def print_list_of_collections():
    Log.cli(main.COLLECTION_NAMES)

def display_options():
    for opt in COMMANDS.keys():
        Log.cli(f"{opt}")

def main_loop():
    processing = True
    while processing:
        display_options()
        user_in = UserInput.user_request(main.PYMONGO_INPUT("Collection"))
        handle_collection_command(user_in)


def init(db):
    print_list_of_collections()
    potential_collection_name = UserInput.user_request("Please pick a Collection to Open.")
    if potential_collection_name in main.COLLECTION_NAMES:
        db_collection = db.get_collection(potential_collection_name)
        Log.cli(f"{potential_collection_name} is ready!")
        # print options here
        for com in COMMANDS.keys():
            Log.cli(com)
        uni = UserInput.user_request(f"Next?")


def query(collection: MCollection, query):
    Log.cli(f"Query = [ {query} ]")
    return collection.query(query)