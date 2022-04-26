import pytest
import requests
from src.api.ilx.ilx_response import Response, ResponseNegative
from src.erp_emulator.erp_ilx import variables
from src.schemas.ilx_schemas import ValidatorPriceD1


@pytest.mark.parametrize('num, data_price_d1, testrail_case_id', [
    (0, variables.data_price_d1, 12511)
])
def test_response_d1_price(ilx_context, num, data_price_d1, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {
        'Authorization': ilx_context.ilx_qa_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        'dsku': data_price_d1[num].get('item'),
        'customerNumber': data_price_d1[num].get('customer')
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_price_d1_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorPriceD1)
    response.validate_response_price_d1(data_price_d1[num])

    print(response)


@pytest.mark.parametrize('num, data_price_d1, testrail_case_id', [
    (1, variables.data_price_d1, 12512)
])
def test_response_d1_price_incorrect_dsku(ilx_context, num, data_price_d1, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {
        'Authorization': ilx_context.ilx_qa_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        'dsku': data_price_d1[num].get('item') + '_test',
        'customerNumber': data_price_d1[num].get('customer')
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_price_d1_url, headers=headers, json=data)
    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)


@pytest.mark.parametrize('num, data_price_d1, testrail_case_id', [
    (2, variables.data_price_d1, 12513)
])
def test_response_d1_price_incorrect_customer(ilx_context, num, data_price_d1, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {
        'Authorization': ilx_context.ilx_qa_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        'dsku': data_price_d1[num].get('item'),
        'customerNumber': data_price_d1[num].get('customer') + '_test'
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_price_d1_url, headers=headers, json=data)
    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)
