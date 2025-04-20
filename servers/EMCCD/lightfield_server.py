import json
from flask import Flask, Response

from lightfield import LightFieldController, LightFieldEmulator

emccd = LightFieldController()
# emccd = LightFieldEmulator(experiment="test")

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'PI EMCCD'
    res['experiment'] = emccd.experiment.Name
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/close")
def close():
    emccd.close()
    res = dict()
    res['success'] = True
    res['message'] = "The LightField app closed"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/clean_count")
def clean_count():
    emccd.clean()
    res = dict()
    res['success'] = True
    res['message'] = "Acquisition count reset to 0"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/acquire/<prefix>")
def acquire(prefix):
    prefix = str(prefix)
    emccd.acquire(prefix=prefix)
    res = dict()
    res['success'] = True
    res['message'] = f"A spectrum saved to {emccd.savedir} with prefix {prefix}"
    res['save_path'] = emccd.savedir
    res['acq_number'] = emccd.count - 1
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')
