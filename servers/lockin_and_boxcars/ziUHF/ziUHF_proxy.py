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
    res['methods'] = ['get_value']
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')


@app.route("/get_value/<averaging_counts>")
def get_value(averaging_counts):
    value, count = uhf.get_value(averaging_counts=int(averaging_counts))
    res = dict()
    res['success'] = True
    res['message'] = "value:float"
    res['value'] = value
    res['count'] = count
    res = json.dumps(res)
    return Response(res, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=50008)