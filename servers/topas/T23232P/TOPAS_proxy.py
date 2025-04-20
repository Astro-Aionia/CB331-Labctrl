import json
from flask import Flask, Response
from TOPAS_REST import Topas4Controller

sn = "T23231P-Demo-7069"

print("Connecting to TOPAS server " + sn)
topas = Topas4Controller(sn)
if topas.baseAddress == None:
    print("Cannot connect to TOPAS " + sn)
topas.getCalibrationInfo()
print(f"TOPAS {sn} connected. Current setup: {topas.interaction}, {topas.wavelength} nm")
_interaction_list = []
for item in topas.interactions:
    _interaction_list.append(item['Type'])

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The proxy is ONLINE"
    res['name'] = 'Demo'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set/<interaction>/<wavelength>")
def set_wavelength(interaction, wavelength):
    interaction = str(interaction)
    interaction_num = _interaction_list.index(interaction)
    wavelength = float(wavelength)
    topas.setWavelength(topas.interactions[interaction_num], wavelength)
    res = dict()
    res['success'] = True
    res['message'] = "Wavelength set to target"
    res['interaction'] = topas.interaction
    res['wavelength'] = topas.wavelength
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)