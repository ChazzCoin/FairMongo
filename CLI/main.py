from fairNLP import Regex
from FLog import LOGGER
from CLI import UserRequest, SearchArticles, cliCollection
from M.MDB import DEFAULT_HOST_INSTANCE

Log = LOGGER.Log("Search", log_level=4)

db = DEFAULT_HOST_INSTANCE

RAW_COLLECTIONS = list(db.core_db.list_collections())
COLLECTION_NAMES = [it["name"] for it in RAW_COLLECTIONS]

WELCOME = f"\n{LOGGER.HEADER}Welcome to pyFongo Command Line!"
PYMONGO_BASE = f"{LOGGER.HEADER}MongoDB@pyFongo -> "
PYMONGO_INPUT = lambda option: f"{LOGGER.HEADER}MongoDB@pyFongo {option} -> "

ENTER_SEARCH = "Enter Search Term: "
SEARCHING = lambda search_term: f"Searching for: [ {search_term} ]"

# -> todo: make this general to the section
SEARCH_OPTIONS = "\nNo More Pages - 2. New Search - 3. Exit - 4. Back/Options\n"

OPTIONS = {"1. Search -> Search Article Database.": ["1", "search", "articles"],
           "2. Get Collection -> Init collection to query.": ["2", "collection"],
           "X. Exit -> Quit pyFongo CLI": ["killThySelf"]}

COMMAND_OPTIONS = {"search": ["1", "search", "articles"],
                   "collection": ["2", "collection"],
                   "exit": ["X", "exit", "kill", "die", "end"] }

COMMANDS_BASE = {"back": ["4", "back", "options"],
                 "exit": ["X", "exit", "kill", "die", "end"]}

class pyFongo:
    processing = True

    @classmethod
    def RUN(cls):
        nc = cls()
        nc.start()

    def start(self):
        print(WELCOME)
        self.main_loop()

    def main_loop(self):
        while self.processing:
            self.display_options()
            user_in = UserRequest.user_request(PYMONGO_BASE)
            self.handle_options_input(user_in)

    def handle_options_input(self, option_input):
        for option in COMMAND_OPTIONS.keys():
            lookUp = COMMAND_OPTIONS[option]
            if Regex.contains_any(lookUp, option_input):
                # -> we have our command, "option"
                func = self.__getattribute__(option)
                return func()

    """ -> Master Commands <- """
    def collection(self):
        cliCollection.cliCollection().main_loop()

    def search(self):
        return SearchArticles.restart_search()

    def exit(self):
        exit()

    def restart(self):
        self.main_loop()

    @staticmethod
    def display_options():
        for opt in OPTIONS.keys():
            Log.cli(f"{opt}")


if __name__ == '__main__':
    c = pyFongo()
    c.start()
