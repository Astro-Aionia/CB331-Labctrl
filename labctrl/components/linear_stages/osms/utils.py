import requests
from functools import wraps

def ignore_connection_error(func):
    @wraps(func)
    def ret(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret
