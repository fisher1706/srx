import pytest
import requests
import random

from src.api.ilx.ilx_response import Response, ResponseNegative
from src.erp_emulator.erp_ilx import variables
from src.schemas.ilx_schemas import ValidatorQuoteEclipse


@pytest.mark.parametrize('num, data_quote_eclipse, testrail_case_id', [
    (0, variables.data_quote_eclipse, 12522),
    (1, variables.data_quote_eclipse, 12523),
])
def test_response_quote_eclipse(ilx_context, num, data_quote_eclipse, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token,
               'Content-Type': 'application/json;charset=utf-8'}

    data = {
        "items": [{
            "dsku": 0,
            "location": {},
            "quantity": str(random.randint(10, 20))
        }],
        "shipTo": {
            "number": str(random.randint(10, 20)),
            "apiWarehouseNumber": str(random.randint(10, 20))
        },
        "orderId": str(random.randint(10, 20)),
        "customer": {},
        "poNumber": data_quote_eclipse[num].get('customer'),
        "warehouse": {
            "number": str(random.randint(10, 20))
        },
        "transactionType": data_quote_eclipse[num].get('status')
        }

    resp = requests.post(url=ilx_context.ilx_data.ilx_quote_eclipse_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorQuoteEclipse)
    response.validate_response_quote_eclipse(data_quote_eclipse[num])
    print(response)


@pytest.mark.parametrize('num, data_quote_eclipse, testrail_case_id', [
    (2, variables.data_quote_eclipse, 12524)
])
def test_response_quote_eclipse_negative(ilx_context, num, data_quote_eclipse, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    customer = data_quote_eclipse[num].get('customer') + '_fail'

    headers = {'Authorization': ilx_context.ilx_qa_token,
               'Content-Type': 'application/json;charset=utf-8'}

    data = {
        "items": [{
            "dsku": 0,
            "location": {},
            "quantity": str(random.randint(10, 20))
        }],
        "shipTo": {
            "number": str(random.randint(10, 20)),
            "apiWarehouseNumber": str(random.randint(10, 20))
        },
        "orderId": str(random.randint(10, 20)),
        "customer": {},
        "poNumber": customer,
        "warehouse": {
            "number": str(random.randint(10, 20))
        },
        "transactionType": data_quote_eclipse[num].get('status')
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_quote_eclipse_url, headers=headers, json=data)
    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)
