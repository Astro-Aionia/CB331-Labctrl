import requests
import json

class RemoteOSMSStage():
    def __init__(self, config, max_retry=3) -> None:
        self.host = config["Host"]
        self.port = config["Port"]
        self.max_retry = max_retry
        self.api_url = 'http://{host}:{port}//'.format(host=self.host, port=self.port)

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

    def set_velocity(self, vel):
        return self.apicall('set_velocity/{:.6f}'.format(vel))
    
    def set_zero(self):
        return self.apicall('set_zero')

    def moveabs(self, pos):
        return self.apicall('moveabs/{:.6f}'.format(pos))

    def moveinc(self, dis):
        return self.apicall('moveinc/{:.6f}'.format(dis))

    def autohome(self):
        return self.apicall('autohome')