from FSON import DICT
from FList import LIST
from FLog.LOGGER import Log
from CLI import UserRequest, main, Commands
from M import MDB
from C import CCollection

Log = Log("cCollection")

""" The Master in control of Mongo Collections """

db = MDB.DEFAULT_HOST_INSTANCE

COMMANDS = {"1. Query -> { key: value } based Query System!": ""}

# FIELDS_IN_COLLECTION = []
class cliCollection:
    className = None
    collection_methods = None

    def handle_collection_command(self, user_in):
        pass

    @staticmethod
    def print_list_of_collections():
        Log.cli(main.COLLECTION_NAMES)

    @staticmethod
    def display_options():
        for opt in COMMANDS.keys():
            Log.cli(f"{opt}")

    def main_loop(self):
        self.collection_methods = self.get_collection_methods()
        processing = True
        while processing:
            # display_options()
            # user_in = UserRequest.user_request(main.PYMONGO_INPUT("Collection"))
            self.init_cCollection()
            # handle_collection_command(user_in)


    def init_cCollection(self):
        self.print_list_of_collections()
        potential_collection_name = UserRequest.user_request("Please pick a Collection to Open.")
        if potential_collection_name in main.COLLECTION_NAMES:
            # init collection
            db.set_ccollection(potential_collection_name)
            Log.cli(f"{potential_collection_name} is ready!")
            FIELDS_IN_COLLECTION = db.get_field_names()
            print(FIELDS_IN_COLLECTION)
            # print options here
            for com in self.collection_methods:
                Log.cli(com)
            # displaying functions from CCollection, trying to use one.
            uni = UserRequest.user_request(f"Your wish?")
            commands = Commands.parse_cli_commands(uni)
            directory_command = LIST.get(0, commands)
            args1 = LIST.get(1, commands)
            args = DICT.get("args", args1)
            result = self.call_collection_method(directory_command, args)
            Log.cli(result)


    def get_collection_methods(self):
        return self.get_method_names(CCollection.CCollection)

    def get_collection_func(self, func):
        return getattr(CCollection.CCollection, func)

    def call_collection_method(self, func, args=None):
        attr_func = self.get_collection_func(func)
        if args:
            return attr_func(args)
        return attr_func()

    def get_method_names(self, className):
        return [func for func in dir(className)
                if self.get_callable(self.get_func(className, func))
                           and not func.startswith("__")
                           and func.islower()
                           and not func.startswith("constructor")
                           and not func.startswith("construct")]

    def get_func(self, className, func):
        return getattr(className, func)

    def get_callable(self, attr):
        return callable(attr)

