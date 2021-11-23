from flask import request
from __main__ import app

@app.route('/external-api/automation/automation/salesOrders', methods = ['POST'])
def sales_orders():
    return submit(request.get_json(), "ORDERED")

@app.route('/external-api/automation/automation/quoteOrders', methods = ['POST'])
def quote_orders():
    return submit(request.get_json(), "QUOTED")

def submit(body, status):
        ids = list()
        MIN = None
        if body is not None:
            if body.get("items") is not None:
                if isinstance(body["items"], list):
                    for item in body["items"]:
                        if "id" in item:
                            ids.append(item["id"])
                    if len(ids) > 0:
                        MIN = min(ids)
        response = {
            "transactionType": status,
            "id": MIN
        }
        return response