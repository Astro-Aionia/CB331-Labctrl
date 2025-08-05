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

@app.route("/move_to/<pos>")
def move_to(pos):
    pos = float(pos)
    stage.move_to(pos)
    res = dict()
    res['success'] = True
    res['message'] = f"Moved to target position {pos} mm"
    res['name'] = 'C863'
    res['position'] = stage.get_position()
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')