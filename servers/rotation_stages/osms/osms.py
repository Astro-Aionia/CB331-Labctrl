import time
import serial

class OSMS:
    def __init__(self, port, baud=9600, timeout=1):
        self.port = port
        self.ser = serial.Serial(self.port, baudrate=baud, timeout=timeout)
        time.sleep(1)
        print(self.ser.readlines())
        self.position = 0 # degrees
        self.distance = 0 # degrees
        self.velocity = 10 # degrees/s
        self.divider = 1 # equal to the settings on the driver
        self.step = 0.005/self.divider # degrees
        self.frequency = int(self.velocity/(self.step)) # Hz
        # self.set_velocity(self.velocity)

    def cmd(self, command, sleep=0.2):
        self.ser.write(command.encode('ascii'))
        response = self.ser.readline().decode()
        print(response.replace('\r\n', ''))
        time.sleep(sleep)
        return response

    def set_divider(self, divider):
        self.divider = int(divider)
        self.step = 0.05/self.divider # degrees
        print(f"Set divider to {divider}, step size is {self.step} degrees. Please check the driver setting to match.")
        self.set_velocity(self.velocity)

    def set_velocity(self, velocity):
        self.velocity = float(velocity)
        self.frequency = int(self.velocity/(self.step)) # Hz
        response = self.cmd(f"SET FREQ {self.frequency}\r\n")
        print(f"Set velocity to {velocity} degrees/s. Frequency is {self.frequency} Hz.")
        return response

    def zero_position(self):
        self.position = 0
        self.distance = 0
        print("Set current position to 0 degrees.")

    def moveabs(self, position):
        print(f"Moving to {position} degrees.")
        self.distance = position - self.position
        step_to_move = int(abs(self.distance/self.step))
        if self.distance >= 0:
            response = self.cmd(f"RUN CCW {step_to_move}\r\n", sleep = step_to_move/self.frequency)
        else:
            response = self.cmd(f"RUN CW {step_to_move}\r\n", sleep = step_to_move/self.frequency)
        self.position = position
        # print("Done.")
        return response
    
    def moveinc(self, distance):
        print(f"Moving by {distance} degrees.")
        self.distance = distance
        step_to_move = int(abs(self.distance/self.step))
        if self.distance >= 0:
            response = self.cmd(f"RUN CCW {step_to_move}\r\n", sleep = step_to_move/self.frequency)
        else:
            response = self.cmd(f"RUN CW {step_to_move}\r\n", sleep = step_to_move/self.frequency)
        self.position = self.position + distance
        # print("Done.")
        return response
    
    def autohome(self):
        print("Homing")
        response = self.moveabs(0)
        return response
    
if __name__ == "__main__":
    osms = OSMS(port="COM21")
    time.sleep(1) # wait for the serial connection to establish
    print("Wait 1 s for opration")
    osms.set_velocity(10)
    #osms.moveabs(30)
    #osms.moveinc(-10)