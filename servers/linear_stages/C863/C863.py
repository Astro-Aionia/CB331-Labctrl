from pipython import GCSDevice
from pipython import pitools

class C863:
    def __init__(self):
        self.pidevice = GCSDevice('C-863')
        self.pidevice.InterfaceSetupDlg()
        print(self.pidevice.qIDN())
        self.position = self.pidevice.qPOS()['1']

    def __del__(self):
        self.pidevice.CloseConnection()

    def get_position(self):
        return self.position

    def move_to(self, position):
        pitools.moveandwait(self.pidevice, ['1'], [position])
        self.position = self.pidevice.qPOS()['1']

if __name__ == "__main__":
    stage = C863()
    stage.move_to(10)
    print(f"Current position: {stage.get_position()}")
    stage.move_to(0)
    print(f"Current position: {stage.get_position()}")
    del stage