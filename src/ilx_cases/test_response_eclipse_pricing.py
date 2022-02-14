import pytest
import requests
from src.api.ilx.ilx_response import Response
from src.erp_emulator.erp_ilx import variables


@pytest.mark.parametrize('eclipse_price_data, testrail_case_id', [
    (variables.data_price_eclipse, 11434)
])
def test_response_eclipse_price(ilx_context, eclipse_price_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {
        'Authorization': ilx_context.ilx_eclipse_price_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        'dsku': eclipse_price_data[0].get('dsku'),
        'customerNumber': eclipse_price_data[0].get('customerNumber'),
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_billing_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)

    print(response)


@pytest.mark.xfail(reason='incorrect data for test')
@pytest.mark.parametrize('eclipse_price_data, testrail_case_id', [
    (variables.data_price_eclipse, 11435)
])
def test_response_eclipse_price_negative(ilx_context, eclipse_price_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    customer = eclipse_price_data[1].get('customerNumber') * 5

    headers = {
        'Authorization': ilx_context.ilx_eclipse_price_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        'dsku': eclipse_price_data[1].get('dsku'),
        'customerNumber': customer,
    }

    resp = requests.post(url=ilx_context.ilx_data.ilx_billing_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)

    print(response)
