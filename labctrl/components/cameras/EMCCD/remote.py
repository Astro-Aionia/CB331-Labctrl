# -*- coding: utf-8 -*-

"""remote.py:
This module provides methods to communicate with a remote
linear stage server.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211110"


import requests
import json

class RemoteEMCCD():
    def __init__(self, config, max_retry=3) -> None:
        self.host = config["Host"]
        self.port = config["Port"]
        self.max_retry = max_retry
        self.api_url = 'http://{host}:{port}/'.format(host=self.host, port=self.port)

    def apicall(self, command):
        for i in range(self.max_retry):
            try:
                apicall = self.api_url + command
                response = requests.get(apicall)
                rc = response.content.decode()
                return json.loads(rc)
            except requests.exceptions.ConnectionError as err:
                print(err)
        print("Error: Cannot connect to remote stage, exceeded max retry {mr}".format(
            mr=self.max_retry))
        raise requests.exceptions.ConnectionError

    def online(self):
        """Tests if the remote stage server is online.
        Does not test if the remote server actually works, however."""
        return self.apicall('')

    def close(self):
        return self.apicall('/close')

    def clean_count(self):
        return self.apicall('/clean_count')

    def reset(self):
        return self.apicall('/reset')

    def acquire(self, filename):
        return self.apicall('/acquire/{filename}'.format(filename=filename))
