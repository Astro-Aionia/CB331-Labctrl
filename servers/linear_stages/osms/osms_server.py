import json
from flask import Flask, Response
from osms import OSMS

stage = OSMS(port="COM14")
app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set_zero/")
def set_zero():
    stage.zero_position()
    res = dict()
    res['success'] = True
    res['message'] = "Set current position to 0 degrees"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set_velocity/<vel>")
def set_velocity(vel):
    vel = float(vel)
    stage.set_velocity(vel)
    res = dict()
    res['success'] = True
    res['message'] = f"Velocity set to {vel}"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set_divider/<div>")
def set_divider(div):
    div = int(div)
    stage.set_divider(div)
    res = dict()
    res['success'] = True
    res['message'] = f"Divider set to {div}"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/moveabs/<pos>")
def moveabs(pos):
    pos = float(pos)
    stage.moveabs(pos)
    res = dict()
    res['success'] = True
    res['message'] = f"Moved to target position {pos} degrees"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/moveinc/<dis>")
def moveinc(dis):
    dis = float(dis)
    stage.moveinc(dis)
    res = dict()
    res['success'] = True
    res['message'] = f"Moved by target distance {dis} degrees"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/autohome")
def autohome():
    stage.autohome()
    res = dict()
    res['success'] = True
    res['message'] = "Moved to Home and reset Home position via limit switch"
    res['name'] = 'OSMS-60YAW'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

