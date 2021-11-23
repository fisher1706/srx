from flask import request
from __main__ import app
from state import State

@app.route('/external-api/automation/automation/salesOrdersStatus/<external_order_id>', methods = ['GET'])
def sales_orders_status_v1(external_order_id):
    response = {
        "response": State.sales_orders_status_v1_items
    }
    return response