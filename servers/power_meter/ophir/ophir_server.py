import json
from flask import Flask, Response
from ophir import ophir

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The proxy is ONLINE"
    res['name'] = "ophir"
    res['methods'] = ['set_range', 'get_range', 'get_data', 'get_value']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/set_range/<int:new_range>")
def set_range(new_range):
    try:
        ophir.set_range(new_range)
        res = dict()
        res['success'] = True
        res['message'] = f"Range set to {new_range}"
    except ValueError as e:
        res = dict()
        res['success'] = False
        res['message'] = str(e)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/get_range")
def get_range():
    try:
        current_range = ophir.get_range()
        res = dict()
        res['success'] = True
        res['message'] = f"Current range: {current_range}"
        res['range'] = current_range
    except ValueError as e:
        res = dict()
        res['success'] = False
        res['message'] = str(e)
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/get_data/<averaging_time>")
def get_data(averaging_time):
    try:
        data = ophir.get_data(averaging_time=float(averaging_time))
        res = dict()
        res['success'] = True
        res['message'] = "Data retrieved successfully"
        res['data'] = data  # Convert numpy array to list for JSON serialization
    except ValueError as e:
        res = dict()
        res['success'] = False
        res['message'] = str(e)
        res['data'] = []
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/get_value/<averaging_time>")
def get_value(averaging_time):
    try:
        value = ophir.get_value(averaging_time=float(averaging_time))
        res = dict()
        res['success'] = True
        res['message'] = "Value retrieved successfully"
        res['value'] = float(value)
    except ValueError as e:
        res = dict()
        res['success'] = False
        res['message'] = str(e)
        res['value'] = None
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50010)