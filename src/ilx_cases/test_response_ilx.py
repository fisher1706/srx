#pylint: disable=W0614

import requests
import pytest
from src.erp_emulator.erp_ilx import variables
from src.api.ilx.ilx_response import Response
from src.schemas.ilx_schemas import Validator
from src.utilities.ilx_utils import generate_url


@pytest.mark.ilx
@pytest.mark.parametrize('case, data_case, url, auth_token', [
    ('case1', variables.data_case_1, variables.url_ilx, variables.ilx_auth),
    ('case2', variables.data_case_2, variables.url_ilx, variables.ilx_auth),
    ('case3', variables.data_case_3, variables.url_ilx, variables.ilx_auth),
    ('case4', variables.data_case_4, variables.url_ilx, variables.ilx_auth),
    ('case5', variables.data_case_5, variables.url_ilx, variables.ilx_auth),
    ('case6', variables.data_case_6, variables.url_ilx, variables.ilx_auth),
    ('case7', variables.data_case_7, variables.url_ilx, variables.ilx_auth),
    ('case8', variables.data_case_8, variables.url_ilx, variables.ilx_auth),
    ('case10', variables.data_case_10, variables.url_ilx, variables.ilx_auth),
    ('case11', variables.data_case_11, variables.url_ilx, variables.ilx_auth)
])
def test_response_ilx_sale_order_v2(case, data_case, url, auth_token):
    headers = {'Authorization': auth_token}

    resp = requests.get(url=generate_url(url, case=case), headers=headers)
    response = Response(resp)

    response.assert_response_status(200)
    response.validate_response_schema(Validator)
    response.validate_response_data(data_case)
