import pytest
import requests

from src.api.ilx.ilx_response import Response, ResponseNegative
from src.erp_emulator.erp_ilx import variables


@pytest.mark.parametrize('case, wmi_data, testrail_case_id', [
    (0, variables.data_wmi_sync, 11421)
])
def test_response_wmi(ilx_context, case, wmi_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {'Authorization': ilx_context.ilx_qa_token}

    params = {
        'startIndex': wmi_data[case]['startIndex'],
        'customerNumber': wmi_data[case]['productId'],
        'shipToNumber': wmi_data[case]['customerId'],
        'pageSize': wmi_data[case]['pageSize']
    }

    resp = requests.get(url=ilx_context.ilx_data.ilx_wmi_url, headers=headers, params=params)

    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_wmi(wmi_data[case])

    print(response)


@pytest.mark.parametrize('case, param, wmi_data, testrail_case_id', [
    (1, 'customerId', variables.data_wmi_sync, 11422),
    (2, 'pageSize', variables.data_wmi_sync, 11423)
])
def test_response_wmi_negative(ilx_context, case, param, wmi_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    if param == 'customerId':
        wmi_data[case].update({"customerId": 666})
    else:
        wmi_data[case].update({"pageSize": 1})

    headers = {'Authorization': ilx_context.ilx_qa_token}

    params = {
        'startIndex': wmi_data[case]['startIndex'],
        'customerNumber': wmi_data[case]['productId'],
        'shipToNumber': wmi_data[case]['customerId'],
        'pageSize': wmi_data[case]['pageSize']
    }

    resp = requests.get(url=ilx_context.ilx_data.ilx_wmi_url, headers=headers, params=params)

    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)
