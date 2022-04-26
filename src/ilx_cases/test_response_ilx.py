import pytest
import requests

from src.api.ilx.ilx_response import Response
from src.erp_emulator.erp_ilx import variables
from src.schemas.ilx_schemas import Validator
from src.utilities.ilx_utils import Utils


@pytest.mark.ilx
@pytest.mark.parametrize('case, data_case, testrail_case_id', [
    ('case1', variables.data_case_1, 10084),
    ('case2', variables.data_case_2, 10085),
    ('case3', variables.data_case_3, 10086),
    ('case4', variables.data_case_4, 10087),
    ('case5', variables.data_case_5, 10088),
    ('case6', variables.data_case_6, 10089),
    ('case7', variables.data_case_7, 10090),
    ('case8', variables.data_case_8, 10091),
    ('case10', variables.data_case_10, 10093),
    ('case11', variables.data_case_11, 10094),
])
def test_response_ilx_sale_order_v2(ilx_context, case, data_case, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_erp_token}
    resp = requests.get(url=Utils.generate_url(ilx_context.ilx_data.ilx_url, case=case), headers=headers)

    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(Validator)
    response.validate_response_data(data_case)

    print(response)
