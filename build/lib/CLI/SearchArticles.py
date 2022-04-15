from fongUtils import Regex
from fongUtils.fongLogger import Log, LogColors
from CLI import UserInput
from Jarticle.jArticles import jArticles

Log = Log("SearchArticles")

WELCOME = f"\n{LogColors.HEADER}Welcome to pyFongo Command Line!"
PYMONGO_INPUT = f"{LogColors.HEADER}MongoDB@pyFongo -> "
ENTER_SEARCH = "Enter Search Term: "
SEARCHING = lambda search_term: f"Searching for: [ {search_term} ]"
SEARCH_OPTIONS = "\nNo More Pages - 2. New Search - 3. Exit - 4. Back/Options\n"
OPTIONS = {"1. Search -> Search Article Database.": "handle_search_input",
           "X. Exit -> Quit pyFongo CLI": "killThySelf"}

db = jArticles.constructor_jarticles()

def handle_search_input(user_in, newPage=False, isFirst=False):
    if isFirst:
        user_search = UserInput.user_request(ENTER_SEARCH)
        perform_search(user_search)
        return False
    if newPage and Regex.contains_any(["1", "next", "page"], user_in):
        return True
    if Regex.contains_any(["2", "new", "search"], user_in):
        user_search = UserInput.user_request(ENTER_SEARCH)
        perform_search(user_search)
        return False
    if Regex.contains_any(["3", "exit", "quit"], user_in):
        exit()
    if Regex.contains_any(["4", "back", "options"], user_in):
        return False
    Log.cli("Bad Input. Restarting...")
    restart_search()

def restart_search():
    search_term = UserInput.user_request(ENTER_SEARCH)
    perform_search(search_term)

def search_loop(records):
    count = len(records)
    Log.cli(f"{count} Articles Found!")
    total_pages = int(count / 10)
    art_count = 1
    current_page = 0
    processing = True

    while processing:
        if current_page > total_pages:
            Log.cli(f"{LogColors.HEADER}\nNo More Pages - 2. New Search - 3. Exit - 4. Back/Options")
            user_in = UserInput.user_request(PYMONGO_INPUT)
            if not handle_search_input(user_in, False):
                return

        # -> Print Results
        Log.cli(f"Page {current_page + 1} of {total_pages}")
        page_records = get_page(records, current_page)
        for i in page_records:
            Log.print_article(art_count, i)
            art_count += 1

        # -> Prepare for next input
        if current_page >= total_pages:
            Log.cli(f"{LogColors.HEADER}\nNo More Pages - 2. New Search - 3. Exit - 4. Back/Options")
            user_in = UserInput.user_request(PYMONGO_INPUT)
            if not handle_search_input(user_in, False):
                return
        else:
            Log.cli(f"{LogColors.HEADER}\n1. Next Page - 2. New Search - 3. Exit - 4. Back/Options")
            user_in = UserInput.user_request(PYMONGO_INPUT)
        if not handle_search_input(user_in, True):
            return
        current_page += 1

def perform_search(search_term):
    Log.i(f"{SEARCHING(search_term=search_term)}")
    records = db.search_unlimited(search_term=search_term)
    if records:
        search_loop(records)
    else:
        Log.e("No Results Found.")
        seearc_request = UserInput.user_request(ENTER_SEARCH)
        perform_search(seearc_request)

def get_page(records, page):
    end_temp = page + 1
    end = end_temp * 10
    start = page * 10
    return records[start:end]