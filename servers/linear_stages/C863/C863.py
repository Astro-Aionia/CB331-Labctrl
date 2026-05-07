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
        self.position = self.pidevice.qPOS()['1']
        return self.position
    
    def set_velocity(self, velocity):
        # self.pidevice.VEL('1', velocity)
        # PI did not provide velocity control for C-863, so we will just set the velocity variable for reference
        print(f"Default velocity.")

    def move_abs(self, position):
        print(f"Moving to {position} mm.")
        pitools.moveandwait(self.pidevice, ['1'], [position])
        self.position = self.pidevice.qPOS()['1']
        print("Done.")

    def move_inc(self, distance):
        print(f"Moving by {distance} mm.")
        pitools.moveandwait(self.pidevice, ['1'], [self.position + distance])
        self.position = self.pidevice.qPOS()['1']
        print("Done.")

    def home(self):
        print("Homing.")
        pitools.moveandwait(self.pidevice, ['1'], [0])
        self.position = self.pidevice.qPOS()['1']
        print("Done.")

if __name__ == "__main__":
    stage = C863()
    stage.move_abs(10)
    print(f"Current position: {stage.get_position()}")
    stage.move_abs(0)
    print(f"Current position: {stage.get_position()}")
    stage.home()
    print(f"Current position: {stage.get_position()}")
    del stage