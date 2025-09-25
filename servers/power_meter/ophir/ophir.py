import win32com.client
import time
import numpy as np

class OphirCom:
    def __init__(self, sn: str):
        self.sn = sn
        self.OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
        self.OphirCOM.StopAllStreams()  # Stop all streams
        self.OphirCOM.CloseAll()  # Close all devices
        self.DeviceList = self.OphirCOM.ScanUSB()
        self.DeviceHandle = self.OphirCOM.OpenUSBDevice(self.sn) if self.DeviceList else None
        self.setted_range = None
        self.range_list  = []
        self.range_num = 0
        if self.OphirCOM.IsSensorExists(self.DeviceHandle, 0):
            print("Device found:", self.DeviceList)
            ranges = self.OphirCOM.GetRanges(self.DeviceHandle, 0)
            self.setted_range = ranges[0] if ranges else None
            self.range_list = ranges[1] if ranges else []
            self.range_num = len(ranges[1])
            print("Available ranges:", ranges[1])
        else:
            print("No device found.")
    
    def __del__(self):
        self.OphirCOM.StopAllStreams()
        self.OphirCOM.CloseAll()
        self.OphirCOM = None

    def get_range(self):
        if self.setted_range is not None:
            # print(f"Available ranges: {self.range_list}")
            print(f"Current set range: {self.range_list[self.setted_range]}")
            return self.setted_range
        else:
            raise ValueError("No range set or device not found.")
        
    def set_range(self, new_range: int):
        if self.setted_range is not None:
            if 0 <= new_range < self.range_num:
                self.OphirCOM.SetRange(self.DeviceHandle, 0, new_range)
                self.setted_range = new_range
                print(f"Range set to: {self.range_list[self.setted_range]}")
            else:
                raise ValueError("Invalid range number.")
        else:
            raise ValueError("No device found or range not set.")
        
    def get_data(self, averaging_time = 0.5):
        self.OphirCOM.StartStream(self.DeviceHandle, 0)
        time.sleep(averaging_time)  # Wait for data to be available
        data = self.OphirCOM.GetData(self.DeviceHandle, 0)
        self.OphirCOM.StopStream(self.DeviceHandle, 0)
        if len(data[0]) > 0:
            return np.array(data[0]).tolist()  # Return the data as a list
            # return data[0][0], data[1][0], data[2][0]
        else:
            raise ValueError("No data available.")
        
    def get_value(self, averaging_time=0.5):
        """Get the average value from the Ophir device."""
        data = self.get_data(averaging_time)
        if data is not None:
            return np.mean(data)
        else:
            raise ValueError("No data received from the device.")


sn = '916803'
ophir = OphirCom(sn)

if __name__ == "__main__":    
    try:
        print("Current Range:", ophir.get_range())
        ophir.set_range(3)  # Example to set range
        print("Data:", ophir.get_data(1))
    except Exception as e:
        print("Error:", e)
    finally:
        del ophir  # Ensure resources are released