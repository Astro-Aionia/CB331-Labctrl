import json
from flask import Flask, Response
from C863 import C863

stage = C863()
app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'C863'
    res['position'] = stage.get_position()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set_velocity/<vel>")
def set_velocity(vel):
    vel = float(vel)
    stage.set_velocity(vel)
    res = dict()
    res['success'] = True
    res['message'] = f"Default velocity"
    res['name'] = 'C863'
    res['position'] = stage.get_position()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    stage.move_abs(pos)
    res = dict()
    res['success'] = True
    res['message'] = f"Moved to target position {pos} mm"
    res['name'] = 'C863'
    res['position'] = stage.get_position()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/moveinc/<dis>")
def moveinc(dis):
    dis = float(dis)
    stage.move_inc(dis)
    res = dict()
    res['success'] = True
    res['message'] = f"Moved by target distance {dis} mm"
    res['name'] = 'C863'
    res['position'] = stage.get_position()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/home")
def home():
    stage.home()
    res = dict()
    res['success'] = True
    res['message'] = f"Homed to position 0 mm"
    res['name'] = 'C863'
    res['position'] = stage.get_position()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')