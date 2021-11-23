from flask import request
from __main__ import app
from state import State

@app.route('/')
def home():
    return "<h1>This is ILX mock server for automation tests<h1>"

@app.route('/external-api/automation/automation', methods = ['GET']) #1.1
def get_available_endpoints():
    response = {
        "data": State.available_endpoints,
        "message": None,
        "code": 200
    }
    return response

@app.route('/set-available-endpoints', methods = ['POST']) #1.1
def set_available_endpoints():
    body = request.get_json()
    State.available_endpoints = body["data"]
    response = {
        "data": State.available_endpoints,
        "message": None,
        "code": 200
    }
    return response

@app.route('/set-sales-orders-status-v1-items', methods = ['POST']) #1.1
def set_sales_orders_status_v1_items():
    body = request.get_json()
    State.sales_orders_status_v1_items = body["data"]
    response = {
        "data": State.sales_orders_status_v1_items,
        "message": None,
        "code": 200
    }
    return response