import json
from flask import Flask, Response
from phase_delayer import PhaseDelayer

phase_delayer = PhaseDelayer(port="COM10")

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The server is ONLINE"
    res['name'] = 'PhaseDelayer'
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/get")
def get_delay():
    res = dict()
    res['success'] = True
    res['message'] = f"Current Delay is {phase_delayer.delay} us."
    res['name'] = 'PhaseDelayer'
    res['delay'] = phase_delayer.delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set/<delay>")
def set_delay(delay):
    delay = int(delay)
    phase_delayer.set_delay(delay)
    res = dict()
    res['success'] = True
    res['message'] = f"Delay set to {phase_delayer.delay} us."
    res['name'] = 'PhaseDelayer'
    res['delay'] = phase_delayer.delay
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')