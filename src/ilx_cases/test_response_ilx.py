# pylint: disable=W0614

import pytest
import requests

from context import Context
from src.api.ilx.ilx_response import Response
from src.erp_emulator.erp_ilx import variables
from src.resources.local_credentials import LocalCredentials
from src.resources.testrail import Testrail
from src.schemas.ilx_schemas import Validator
from src.utilities.ilx_utils import Utils


@pytest.fixture(scope="function")
def ilx_data():
    cred = LocalCredentials('ilx')
    context = Context()

    context.testrail_run_id = 282
    ilx_testrail = {
        'case1': 10084, 'case2': 10085, 'case3': 10086, 'case4': 10087, 'case5': 10088,
        'case6': 10089, 'case7': 10090, 'case8': 10091, 'case9': 10092, 'case10': 10093,
        'case11': 10094, 'case12': 10095, 'case13': 10096, 'case14': 10097
    }

    return cred, context, ilx_testrail


@pytest.mark.ilx
@pytest.mark.parametrize('case, data_case', [
    ('case1', variables.data_case_1),
    ('case2', variables.data_case_2),
    ('case3', variables.data_case_3),
    ('case4', variables.data_case_4),
    ('case5', variables.data_case_5),
    ('case6', variables.data_case_6),
    ('case7', variables.data_case_7),
    ('case8', variables.data_case_8),
    ('case10', variables.data_case_10),
    ('case11', variables.data_case_11),
])
def test_response_ilx_sale_order_v2(case, data_case, ilx_data):
    credentials = ilx_data[0]
    context = ilx_data[1]
    ilx_case = ilx_data[2]

    headers = {'Authorization': credentials.ilx_auth}
    resp = requests.get(url=Utils.generate_url(credentials.ilx_url, case=case), headers=headers)
    response = Response(resp)

    response.assert_response_status(200)
    response.validate_response_schema(Validator)
    response.validate_response_data(data_case)
    print(response.__str__())

    context.testrail_case_id = ilx_case.get(case)
    context.testrail_comment = f"Test passed with data: {response.data}"

    testrail = Testrail(credentials.testrail_email, credentials.testrail_password)
    testrail.add_result_for_case(context.testrail_run_id, context.testrail_case_id,
                                 context.testrail_status_id, context.testrail_comment)
