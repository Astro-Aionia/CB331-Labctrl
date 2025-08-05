import time
import serial

class Servo:
    def __init__(self, port, baud=115200, timeout=1):
        self.port = port
        self.ser = serial.Serial(self.port, baudrate=baud, timeout=timeout)
        self.position = 0 # mm
        self.distance = 0 # mm
        self.velocity = 30 # mm/s

    def __del__(self):
        self.close()

    def open(self):
        self.ser.open()

    def close(self):
        self.ser.close()

    def cmd(self, command, sleep=1):
        self.ser.write(command.encode('ascii'))
        response = self.ser.readline().decode()
        print(response)
        time.sleep(sleep)
        return response

    def hareware_position(self):
        return self.cmd("HWPOS\r")

    def set_velocity(self, velocity):
        self.velocity = float(velocity)
        print(f"Set velocity to {velocity} mm/s.")

    def moveabs(self, position):
        print(f"Moving to {position} mm/s.")
        self.distance = abs(position - self.position)
        response = self.cmd(f"MOVEABS {position} {self.velocity}\r", sleep= self.distance/self.velocity)
        self.position = position
        print("Done.")
        return response

    def moveinc(self, distance):
        print(f"Moving by {distance} mm/s.")
        self.distance = abs(distance)
        response = self.cmd(f"MOVEINC {distance} {self.velocity}\r", sleep= self.distance/self.velocity)
        self.position = self.position + distance
        print("Done.")
        return response

    def autohome(self):
        print("Homing")
        self.distance = abs(0 - self.position)
        response = self.cmd("HOMECMD\r", sleep=120)
        self.position = 0
        print("Done.")
        return response

if __name__ == "__main__":
    servo = Servo(port="COM8")
    servo.set_velocity(30)
    servo.moveabs(0)
    servo.moveinc(10)
    print(servo.position)
