import json
from flask import Flask, Response

from camera import ToupCamController, ToupCamEmulator

camera = ToupCamController()
# camera = ToupCamEmulator()
camera.open()
# camera.save(path='C:\\Users\\zhenggroup\\Desktop\\New')

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'ToupTekCamera'
    res['methods'] = ['open', 'close', 'save']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route('/open')
def opencam():
    res = dict()
    res['success'] = True
    res['message'] = "Camera Opened"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route('/close')
def closecam():
    camera.close()
    res = dict()
    res['success'] = True
    res['message'] = "Camera Closed"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route('/clean_count')
def clean_count():
    camera.clean_count()
    res = dict()
    res['success'] = True
    res['message'] = "Acquisition number reset to 0"
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route('/save/<path:save_path>')
def save(save_path):
    camera.save(path=save_path)
    res = dict()
    res['success'] = True
    res['message'] = "An image acquired."
    res['acq_number'] = camera.count - 1
    res['save_path'] = save_path
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')