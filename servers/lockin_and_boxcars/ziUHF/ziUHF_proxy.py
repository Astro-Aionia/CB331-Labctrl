# -*- coding: utf-8 -*-

"""ziUHF_proxy.py:
This module provides web proxy for
a remote ziUHF
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211130"

import json
from flask import Flask, Response
from ziUHF import uhf

app = Flask(__name__)

@app.route("/")
def online():
    res = dict()
    res['success'] = True
    res['message'] = "The proxy is ONLINE"
    res['name'] = "ziUHF"
    res['methods'] = ['get_value', 'get_data']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/get_value/<averaging_time>")
def get_value(averaging_time=0.1):
    value, reference = uhf.get_value(averaging_time=float(averaging_time))
    res = dict()
    res['success'] = True
    res['message'] = "value:float"
    res['value'] = value
    res['reference'] = reference
    res['averaging_time'] = averaging_time
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

@app.route("/get_data/<averaging_time>")
def get_data(averaging_time=0.1):
    data, reference = uhf.get_data(averaging_time=float(averaging_time))
    res = dict()
    res['success'] = True
    res['message'] = "data:list"
    res['data'] = data
    res['reference'] = reference
    res['averaging_time'] = averaging_time
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50008)