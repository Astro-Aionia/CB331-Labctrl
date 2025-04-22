import json
from flask import Flask, Response
from servo import Servo

stage = Servo(port="COM8")
app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'CDHD2'
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
    res['message'] = "Velocity set"
    res['name'] = 'CDHD2'
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
    res['message'] = f"Moved to target position {pos} mm"
    res['name'] = 'CDHD2'
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
    res['message'] = f"Moved by target distance {dis} mm"
    res['name'] = 'CDHD2'
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
    res['name'] = 'CDHD2'
    res['position'] = stage.position
    res['velocity'] = stage.velocity
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')