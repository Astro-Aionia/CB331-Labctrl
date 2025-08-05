# Add needed dll references
import os
import sys
import time
import numpy as np

sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
import clr
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# Import System.IO for saving and opening files
from System.IO import *
# Import c compatible List and String
from System import String
from System.Collections.Generic import List

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import DeviceType, ExperimentSettings, CameraSettings, RegionOfInterest, AdcQuality, SpectrometerSettings

class LightFieldController():
    def __init__(self, experiment: str = None, interface=True):
        self.auto = None
        self.experiment = None
        self.count = 0
        try:
            self.auto = Automation(interface, List[String]())
            self.experiment = self.auto.LightFieldApplication.Experiment
            if not experiment is None:
                self.experiment.Load(experiment)
                # self.setup = experiment
                self.savedir = self.experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)
            print(f"Successfully loaded experiment {self.experiment.Name}. Current file path: {self.savedir}")
        except Exception as err:
            print(err)

    def close(self):
        print('Releasing LightFieldApp object...')
        # self.auto.Dispose()
        if not self.auto is None:
            print("Closing App...")
            if not self.auto.IsDisposed:
                self.auto.Dispose()
            print("LightField app has been closed.")

    def get_dir(self):
        return self.experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)

    def acquire(self, path=None, filename='spe'):
        if path == None:
            path = self.experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationDirectory, path)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, filename+"-"+str(self.count).zfill(6))
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationAttachIncrement, False)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate, False)
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, False)
        self.savedir = self.experiment.GetValue(ExperimentSettings.FileNameGenerationDirectory)
        if self.experiment.IsReadyToRun:
            self.experiment.Acquire()
            time.sleep(self.acquire_time())
            if self.experiment.GetValue(ExperimentSettings.OnlineExportEnabled):
                self.frame_avg(filename=filename)
            print("Image {num} saved to {path}".format(num=filename, path=self.savedir))
            self.count = self.count + 1
        else:
            print("Devices is not ready.")

    def acquire_time(self):
        frames = self.experiment.GetValue(ExperimentSettings.AcquisitionFramesToStore)
        exposure = self.experiment.GetValue(CameraSettings.ShutterTimingExposureTime)
        return float(frames)*(float(exposure)*0.001+0.1)+0.5

    def reset_increment(self):
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationIncrementNumber , "0")

    def frame_avg(self, filename):
        filelist = os.listdir(self.get_dir())
        csvlist = []
        for file in filelist:
            if filename in file and '.csv' in file:
                csvlist.append(file)
        data = np.zeros((1600, 2))
        frame_num = 0
        for file in csvlist:
            data = data + np.loadtxt(self.get_dir() + '\\' + file, delimiter=',')
            frame_num = frame_num + 1
        data = data / frame_num
        np.savetxt(self.get_dir() + '\\' + filename + '.csv', data, delimiter=',')
        return data

    def clean(self):
        self.count = 0
        self.experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, '')
        print("Acquisition number reset to 0.")


class LightFieldEmulator():
    def __init__(self, experiment: str = None, interface=True):
        self.count = 0
        self.experiment.Name = experiment
        self.savedir = "C:\\Users\\zhenggroup\\Documents\\LightField"

    def close(self):
        print('Releasing LightFieldApp object...')
        print("LightField app has been closed.")

    def acquire(self, path="C:\\Users\\zhenggroup\\Documents\\LightField", prefix='spe', export=False):
        filename = prefix + str(self.count).zfill(5)
        print("Image {filename} saved to {path}".format(filename=filename, path=self.savedir))
        self.count = self.count + 1

    def clean(self):
        self.count = 0
        print("Acquisition number reset to 0.")

if __name__ == '__main__':
    app = LightFieldController(experiment="SFG")
    print(app.acquire("test"))
    app.close()
