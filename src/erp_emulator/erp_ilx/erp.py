from __main__ import app #pylint: disable=E0611
from flask import request

from utils import *
from variables import *


@app.route('/external-api/test-full2/test-full2/vmilistsync', methods=['GET'])
def vmi_list_sync():
    startIndex = request.args.get('startIndex')
    customerNumber = request.args.get('customerNumber')
    shipToNumber = request.args.get('shipToNumber')
    pageSize = request.args.get('pageSize')

    if (startIndex is None or customerNumber is None or shipToNumber is None or pageSize is None):
        response = {
            "error": "error"
        }
        return response, 400
    else:
        response = {
            "results": [
                {
                    "dsku": "VIRTUAL 2",
                    "locationName1": "locationName",
                    "locationValue1": "value",
                    "csku": "VIRTUAL 2 updated2",
                    "min": 1,
                    "max": 101,
                    "id": "123"
                },
                {
                    "dsku": "BANANA DSKU",
                    "locationName1": "name",
                    "locationValue1": "value",
                    "csku": "Banana 98072376",
                    "min": 1,
                    "max": 99,
                    "id": "333"
                },
                {
                    "dsku": "APPLE DSKU",
                    "locationName1": "locationName 98072376",
                    "locationValue1": "value",
                    "csku": "Appl2",
                    "min": 1,
                    "max": 23,
                    "id": "234"
                },
                {
                    "dsku": "DERP",
                    "locationName1": "derp loc name 1",
                    "locationValue1": "loc value1",
                    "csku": "updated name derp(only 98072376)",
                    "min": 1,
                    "max": 11,
                    "id": "746837"
                },
                {
                    "dsku": "test",
                    "locationName1": "",
                    "locationValue1": "",
                    "csku": "ctest 98072376",
                    "min": 1,
                    "max": 11,
                    "id": "444"
                }

            ],
            "metadata": {
                "startIndex": int(startIndex),
                "pageSize": int(pageSize),
                "totalItems": 667
            }
        }
    return response, 200


@app.route('/external-api/test-full2/test-full2', methods=['GET'])
def get_full2():
    response = {
        "data": [
            "getPricing",
            "quoteOrders",
            "salesOrders",
            "vmilistsync",
            "searchProduct"
        ],
        "message": None,
        "code": 200
    }
    return response


@app.route('/external-api/test-full2/test-full2/SalesOrdersV2/<order_id>', methods=['GET'])
def get_order(order_id):
    response = {
        "updateKey": "BDE70949B9362887889DD492808EA2B3",
        "id": order_id
    }

    error_response = {
        "error": "error"
    }

    if (order_id == "case1"):
        generations, lines = create_data_order(data_case_1)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case2"):
        generations, lines = create_data_order(data_case_2)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case3"):
        generations, lines = create_data_order(data_case_3)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case4"):
        generations, lines = create_data_order(data_case_4)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case5"):
        generations, lines = create_data_order(data_case_5)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case6"):
        generations, lines = create_data_order(data_case_6)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case7"):
        generations, lines = create_data_order(data_case_7)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case8"):
        generations, lines = create_data_order(data_case_8)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case10"):
        generations, lines = create_data_order(data_case_10)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case11"):
        generations, lines = create_data_order(data_case_11)
        response["generations"] = generations
        response["lines"] = lines

        return response

    if (order_id == "case12"):
        generations, lines = create_data_order(data_case_12)
        response["generations"] = generations
        response["lines"] = lines

        return response

    return error_response, 400


