import os
import sys

from __main__ import app #pylint: disable=E0611
from flask import request

sys_path = os.path.join(os.path.dirname(__file__), '../../..')
sys.path.append(sys_path)

from src.utilities.generate_data_test import GenerateInforOrderStatusV2 as Infor #pylint: disable=C0413
from src.utilities.generate_data_test import GenerateVmiList as Vmi #pylint: disable=C0413
from src.erp_emulator.erp_ilx.utils import UtilsServerIlx as ServUtils #pylint: disable=C0413
from src.erp_emulator.erp_ilx.variables import * #pylint: disable=C0413,W0401

# from utils import UtilsServerIlx as ServUtils
# from variables import *


@app.route('/external-api/test-full2/test-full2/syndicalist', methods=['GET'])
def vmi_list_sync():
    start_index = request.args.get('startIndex')
    customer_number = request.args.get('customerNumber')
    ship_to_number = request.args.get('shipToNumber')
    page_size = request.args.get('pageSize')

    if start_index is None or customer_number is None or ship_to_number is None or page_size is None:
        response = {
            "error": "error"
        }

        status_code = 400
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
                "startIndex": int(start_index),
                "pageSize": int(page_size),
                "totalItems": 667
            }
        }

        status_code = 200

    return response, status_code


@app.route('/external-api/test-full2/test-full2', methods=['GET'])
def get_full2():
    response = {
        "inbox": [
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


@app.route('/external-api/test-full2/test-full2/SalesOrders/<order_id>', methods=['GET'])
def get_order(order_id):
    response = {
        "updateKey": "BDE70949B9362887889DD492808EA2B3",
        "id": order_id
    }

    error_response = {
        "error": "error"
    }

    if order_id == "case1":
        generations, lines = ServUtils.create_data_order(data_case_1)
    elif order_id == "case2":
        generations, lines = ServUtils.create_data_order(data_case_2)
    elif order_id == "case3":
        generations, lines = ServUtils.create_data_order(data_case_3)
    elif order_id == "case4":
        generations, lines = ServUtils.create_data_order(data_case_4)
    elif order_id == "case5":
        generations, lines = ServUtils.create_data_order(data_case_5)
    elif order_id == "case6":
        generations, lines = ServUtils.create_data_order(data_case_6)
    elif order_id == "case7":
        generations, lines = ServUtils.create_data_order(data_case_7)
    elif order_id == "case8":
        generations, lines = ServUtils.create_data_order(data_case_8)
    elif order_id == "case10":
        generations, lines = ServUtils.create_data_order(data_case_10)
    elif order_id == "case11":
        generations, lines = ServUtils.create_data_order(data_case_11)
    else:
        return error_response, 400

    response.update({"generations": generations, "lines": lines})
    return response


@app.route('/external-api/test-full2/test-full2/sxapioegetsingleorderv3', methods=['GET', 'POST'])
def get_order_infor():
    order_number  = request.get_json().get('request').get('orderNumber')
    response = {'error': f'orderNumber: {order_number} - not found'}

    for data in data_infor:
        if str(data.get('orderno')) == str(order_number):
            return Infor.generate_resp_infor(data, Infor.online_field, Infor.response)

    return response, 400


@app.route('/external-api/test-full2/test-full2/CustomerPartNumbers', methods=['GET'])
def get_vmi_sync():
    customer_id = request.args['customerId']
    page_size = request.args['pageSize']

    response = {'error': f'incorrect data for customerId: {customer_id}'}

    for data in data_wmi_sync:
        if str(data['customerId']) == customer_id and str(data['pageSize']) == page_size:
            resp = Vmi().create_response_vmi(data)
            return resp

    return response, 400
