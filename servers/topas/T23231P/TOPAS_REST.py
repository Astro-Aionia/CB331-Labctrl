import sys
import requests
from Topas4Locator import Topas4Locator

class Topas4Controller:
    baseAddress = None
    interactions = None
    interaction_name_list = {}
    interaction = None
    wavelength = None

    def __init__(self, serialNumber):
        locator = Topas4Locator()
        availableDevices = locator.locate()
        match = next((obj for obj in availableDevices if obj['SerialNumber']==serialNumber), None)
        if match is None:
            print ('Device with serial number %s not found' % serialNumber)
        else:
            self.baseAddress = match['PublicApiRestUrl_Version0']
            print(f"Connected to {serialNumber}")
            # self.getCalibrationInfo()
            self.interaction = self.get("/Optical/WavelengthControl/Output/Interaction").json()
            self.wavelength = self.get("/Optical/WavelengthControl/Output/Wavelength").json()
            # print(f"Current setup: {self.interaction}, {self.wavelength} nm")

    def put(self, url, data):
        return requests.put(self.baseAddress + url, json =data)
    def post(self, url, data):
        return requests.post(self.baseAddress + url, json =data)
    def get(self, url):
        return requests.get(self.baseAddress + url)
    
    def changeShutter(self) -> bool:
        isShutterOpen = self.get('/ShutterInterlock/IsShutterOpen').json()
        # line = input(r"Do you want to " + ("close" if isShutterOpen  else "open") + r" shutter? (Y\N)").upper()
        # if line == "Y" or line == "YES":
        self.put('/ShutterInterlock/OpenCloseShutter', not isShutterOpen)
        return isShutterOpen

    def getCalibrationInfo(self):
        self.interactions = self.get('/Optical/WavelengthControl/ExpandedInteractions').json()
        print("Available interactions:")
        for item in self.interactions:
           print(item['Type'] + " %d - %d nm" % (item['OutputRange']['From'], item['OutputRange']['To']))
        if len(self.interactions) == 0:
            print("No interaction")

    def setWavelength(self, interaction, wavelength):
        print("Setting wavelength to {wv} with interaction {interaction}".format(wv=wavelength, interaction=interaction['Type']))
        if interaction['OutputRange']['From'] < wavelength < interaction['OutputRange']['To']:
            response = self.put('/Optical/WavelengthControl/SetWavelength', {'Interaction':interaction['Type'], 'Wavelength':wavelength})
            self.waitTillWavelengthIsSet()
            print("Wavelength set, response:", response)
            self.interaction = interaction['Type']
            self.wavelength = wavelength
        else:
            print("Wavelength out of range.")

    def waitTillWavelengthIsSet(self):
       """
       Waits till wavelength setting is finished.  If user needs to do any manual
       operations (e.g.  change wavelength separator), inform him/her and wait for confirmation.
       """
       while(True):
        s = self.get('/Optical/WavelengthControl/Output').json()
        sys.stdout.write("\r %d %% done" % (s['WavelengthSettingCompletionPart'] * 100.0))
        if s['IsWavelengthSettingInProgress'] == False or s['IsWaitingForUserAction']:
            break
       state = self.get('/Optical/WavelengthControl/Output').json()
       if state['IsWaitingForUserAction']:
          print("\nUser actions required. Press enter key to confirm.")
          #inform user what needs to be done
          for item in state['Messages']:
             print(item['Text'] + ' ' + ('' if item['Image'] is None else ', image name: ' + item['Image']))
          sys.stdin.read(1)#wait for user confirmation
          # tell the device that required actions have been performed.  If shutter was open before setting wavelength it will be opened again
          self.put('/Optical/WavelengthControl/FinishWavelengthSettingAfterUserActions', {'RestoreShutter':True})
       print("Done setting wavelength")

if __name__ == "__main__":
    topas = Topas4Controller("T23231P-Demo-7069")
    topas.getCalibrationInfo()
    print(f"TOPAS connected {topas.baseAddress}. Current setup: {topas.interaction}, {topas.wavelength} nm")
    print(type('132'))
    _interaction_list = []
    for item in topas.interactions:
        _interaction_list.append(item['Type'])
    print(_interaction_list)