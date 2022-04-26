import pytest
import requests

from src.api.ilx.ilx_response import Response, ResponseNegative
from src.erp_emulator.erp_ilx import variables
from src.utilities.ilx_utils import Utils
from src.schemas.ilx_schemas import ValidatorGerrie


@pytest.mark.parametrize('num, gerrie_data, testrail_case_id', [
    (0, variables.data_gerrie_electric, 11438),
    (1, variables.data_gerrie_electric, 11439),
    (2, variables.data_gerrie_electric, 11440),
    (3, variables.data_gerrie_electric, 11441)
])
def test_response_gerrie_electric(ilx_context, num, gerrie_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token}
    params = {'customerId': gerrie_data[num]['customerNumber']}

    resp = requests.get(url=Utils.generate_url(ilx_context.ilx_data.ilx_gerrie_url,
                                               orderId=gerrie_data[num]['orderNumber']), headers=headers, params=params)

    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorGerrie)
    response.validate_response_gerrie(gerrie_data[num])

    print(response)


@pytest.mark.parametrize('num, gerrie_data, testrail_case_id', [
    (4, variables.data_gerrie_electric, 11445)
])
def test_response_gerrie_electric_negative(ilx_context, num, gerrie_data, testrail_case_id):
    customer_id = None
    order_id = None
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token}

    if num == 4:
        customer_id = gerrie_data[num].get('customerNumber') + '_fail'
        order_id = gerrie_data[num].get('orderNumber') + '_fail'

    params = {'customerId': customer_id}

    resp = requests.get(url=Utils.generate_url(ilx_context.ilx_data.ilx_gerrie_url,
                                               orderId=order_id), headers=headers, params=params)

    response = ResponseNegative(resp)
    response.assert_response_negative_status(400)

    print(response)
