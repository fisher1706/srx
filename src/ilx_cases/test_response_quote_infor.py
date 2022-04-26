import pytest
import requests

from src.api.ilx.ilx_response import Response, ResponseNegative
from src.erp_emulator.erp_ilx import variables
from src.schemas.ilx_schemas import ValidatorQuoteInfor


@pytest.mark.parametrize('num, data_quote_infor, testrail_case_id', [
    (0, variables.data_quote_infor, 11451),
    (1, variables.data_quote_infor, 11452)
])
def test_response_quote_infor(ilx_context, num, data_quote_infor, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token,
               'Content-Type': 'application/json;charset=utf-8'}

    data = {
        "items": [{
            "dsku": "input value",
            "location": {},
            "quantity": "input value"
        }],
        "shipTo": {
            "number": "input value",
            "apiWarehouseNumber": "input value"
        },
        "orderId": "input value",
        "customer": {
            "number": data_quote_infor[num].get('custNo')
        },
        "warehouse": {
            "number": "input value"
        },
        "transactionType": data_quote_infor[num].get('transactionType')
        }

    resp = requests.post(url=ilx_context.ilx_data.ilx_quote_infor_url, headers=headers, json=data)

    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorQuoteInfor)
    response.validate_response_quote_infor(data_quote_infor[num])
    print(response)


@pytest.mark.parametrize('num, data_quote_infor, testrail_case_id', [
    (2, variables.data_quote_infor, 11453)
])
def test_response_quote_infor_negative(ilx_context, num, data_quote_infor, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    number = data_quote_infor[num].get('custNo') + '_fail'

    headers = {'Authorization': ilx_context.ilx_qa_token,
               'Content-Type': 'application/json;charset=utf-8'}

    data = {
        "items": [{
            "dsku": "input value",
            "location": {},
            "quantity": "input value"
        }],
        "shipTo": {
            "number": "input value",
            "apiWarehouseNumber": "input value"
        },
        "orderId": "input value",
        "customer": {
            "number": number
        },
        "warehouse": {
            "number": "input value"
        },
        "transactionType": data_quote_infor[num].get('transactionType')
        }

    resp = requests.post(url=ilx_context.ilx_data.ilx_quote_infor_url, headers=headers, json=data)

    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)
