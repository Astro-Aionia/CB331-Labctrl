import requests
from functools import wraps

def ignore_connection_error(func):
    @wraps(func)
    def ret(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except requests.exceptions.ConnectionError as e:
            print("Connection failed")
    return ret
