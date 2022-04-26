import pytest
import requests
import random

from src.api.ilx.ilx_response import Response, ResponseNegative
from src.erp_emulator.erp_ilx import variables
from src.schemas.ilx_schemas import ValidatorInforBilling


@pytest.mark.parametrize('data_infor_billing, testrail_case_id', [
    (variables.data_infor_billing, 12514),
])
def test_response_infor_billing(ilx_context, data_infor_billing, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token,
               'Content-Type': 'application/json;charset=utf-8'}

    data = {
        "items": [{
            "dsku": data_infor_billing['sellerProd'],
            "location": {},
            "quantity": data_infor_billing['qtyOrd']
        }],
        "shipTo": {
            "number": data_infor_billing['shipToNo'],
        },
        "orderId": str(random.randint(10, 20)),
        "customer": {},

        "billingId": str(random.randint(10, 20))
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_infor_billing_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorInforBilling)
    response.validate_response_infor_billing(data_infor_billing)

    print(response)


@pytest.mark.parametrize('type_error, data_infor_billing, testrail_case_id', [
    ("dsku", variables.data_infor_billing, 12515),
    ("quantity", variables.data_infor_billing, 12516),
    ("number", variables.data_infor_billing, 12517)
])
def test_response_infor_billing_negative(ilx_context, type_error, data_infor_billing, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token,
               'Content-Type': 'application/json;charset=utf-8'}

    data = None

    if type_error == "dsku":
        data = {
            "items": [{
                "dsku": 'test_' + data_infor_billing['sellerProd'],
                "location": {},
                "quantity": data_infor_billing['qtyOrd']
            }],
            "shipTo": {
                "number": data_infor_billing['shipToNo'],
            },
            "orderId": str(random.randint(10, 20)),
            "customer": {},

            "billingId": str(random.randint(10, 20))
        }

    if type_error == "quantity":
        data = {
            "items": [{
                "dsku": data_infor_billing['sellerProd'],
                "location": {},
                "quantity": 'test_' + data_infor_billing['qtyOrd']
            }],
            "shipTo": {
                "number": data_infor_billing['shipToNo'],
            },
            "orderId": str(random.randint(10, 20)),
            "customer": {},

            "billingId": str(random.randint(10, 20))
        }

    if type_error == "number":
        data = {
            "items": [{
                "dsku": data_infor_billing['sellerProd'],
                "location": {},
                "quantity": data_infor_billing['qtyOrd']
            }],
            "shipTo": {
                "number": 'test_' + data_infor_billing['shipToNo'],
            },
            "orderId": str(random.randint(10, 20)),
            "customer": {},

            "billingId": str(random.randint(10, 20))
        }

    resp = requests.post(url=ilx_context.ilx_data.ilx_infor_billing_url, headers=headers, json=data)
    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)
