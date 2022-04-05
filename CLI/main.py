from Futils import Regex
from Futils.rsLogger import Log, LogColors
# from Jarticle.jArticles import jArticles
from CLI import UserInput, SearchArticles

Log = Log("Search", log_level=4)
# db = jArticles.constructor()

WELCOME = f"\n{LogColors.HEADER}Welcome to pyFongo Command Line!"
PYMONGO_INPUT = f"{LogColors.HEADER}MongoDB@pyFongo -> "
ENTER_SEARCH = "Enter Search Term: "
SEARCHING = lambda search_term: f"Searching for: [ {search_term} ]"
SEARCH_OPTIONS = "\nNo More Pages - 2. New Search - 3. Exit - 4. Back/Options\n"
OPTIONS = {"1. Search -> Search Article Database.": "handle_search_input",
           "X. Exit -> Quit pyFongo CLI": "killThySelf"}


def display_options():
    for opt in OPTIONS.keys():
        Log.cli(f"{opt}")

def handle_options_input(option_input):
    if Regex.contains_any(["1", "search"], option_input):
        SearchArticles.handle_search_input(user_in=option_input, isFirst=True)
    elif Regex.contains_any(["X", "exit", "kill", "die", "end"], option_input):
        exit()

def main_loop():
    processing = True
    while processing:
        display_options()
        user_in = UserInput.user_request(PYMONGO_INPUT)
        handle_options_input(user_in)

def start():
    print(WELCOME)
    main_loop()
    # search_term = user_request(ENTER_SEARCH)
    # perform_search(search_term)


def restart():
    # print(WELCOME)
    search_term = UserInput.user_request(ENTER_SEARCH)
    SearchArticles.perform_search(search_term)


if __name__ == '__main__':
    start()
