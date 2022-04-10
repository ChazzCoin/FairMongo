from Futils.rsLogger import LogColors

def user_request(request):
    return input(f"{LogColors.HEADER}{request}")