import time
import random
import pytest
import requests
from src.api.ilx.ilx_response import Response
from src.schemas.ilx_schemas import ValidatorBilling
from src.erp_emulator.erp_ilx import variables
from src.utilities.ilx_utils import Utils


@pytest.mark.parametrize('customer_num, billing_data, testrail_case_id', [
    ('test_01', variables.data_billing, 11431),
    ('test_02', variables.data_billing, 11432),
])
def test_response_billing(ilx_context, customer_num, billing_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {
        'Authorization': ilx_context.ilx_billing_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        "date": str(int(time.time())),
        "billingLines": [{
            "price": '{:.2f}'.format(random.randint(1000, 2000) * 0.01), #pylint:disable=C0209
            "comment": Utils.random_str(size=10),
            "quantity": str(random.randint(10, 200)),
            "salesForceSku": str(random.randint(10, 200))
        }],
        "externalDistributorNumber": customer_num
    }


    resp = requests.post(url=ilx_context.ilx_data.ilx_billing_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorBilling)
    response.validate_response_billing(Utils.get_data_billing(customer_num, billing_data))

    print(response)

@pytest.mark.xfail(reason='incorrect data for test')
@pytest.mark.parametrize('customer_num, billing_data, testrail_case_id', [
    ('test_01', variables.data_billing, 11433),
])
def test_response_billing_negative(ilx_context, customer_num, billing_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    customer_num += '_fail'

    headers = {
        'Authorization': ilx_context.ilx_billing_token,
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        "date": str(int(time.time())),
        "billingLines": [{
            "price": '{:.2f}'.format(random.randint(1000, 2000) * 0.01), #pylint:disable=C0209
            "comment": Utils.random_str(size=10),
            "quantity": str(random.randint(10, 200)),
            "salesForceSku": str(random.randint(10, 200))
        }],
        "externalDistributorNumber": customer_num
    }


    resp = requests.post(url=ilx_context.ilx_data.ilx_billing_url, headers=headers, json=data)
    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorBilling)
    response.validate_response_billing(Utils.get_data_billing(customer_num, billing_data))
    print(response)
