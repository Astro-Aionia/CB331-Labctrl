"""
An electrical phase delay generator produced by qmztech.
Phase delay can generator a delay from 1-990 us with serial command "#SET:{delay}%\n".
Only int variable can be written for now
"""

import serial

class PhaseDelayer:
    def __init__(self, port, baud=115200, timeout=1):
        self.port = port
        self.ser = serial.Serial(self.port, baudrate=baud, timeout=timeout)
        self.ser.write(("#SET:1%\n").encode("utf-8"))
        self.delay = 1 # us

    def __del__(self):
        self.close()

    def open(self):
        self.ser.open()

    def close(self):
        self.ser.close()

    def get_delay(self):
        return self.delay
    
    def set_delay(self, delay: int):
        if 1 <= delay <= 990:
            self.ser.write((f"#SET:{delay}%\n").encode("ascii"))
            self.delay = delay
        else:
            print("Error: delay out of range.")

if __name__ == "__main__":
    phase_delayer = PhaseDelayer(port="COM10")
    print(phase_delayer.get_delay())
    phase_delayer.set_delay(995)
    phase_delayer.set_delay(3)
    print(phase_delayer.get_delay())