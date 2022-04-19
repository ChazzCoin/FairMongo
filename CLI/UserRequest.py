from fongUtils import LOGGER

def user_request(request):
    return input(f"{LOGGER.HEADER}{request}")