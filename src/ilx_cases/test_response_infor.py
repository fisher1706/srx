import pytest
import requests

from src.api.ilx.ilx_response import Response
from src.erp_emulator.erp_ilx import variables
from src.utilities.ilx_utils import Utils


@pytest.mark.parametrize('order_no, infor_data, testrail_case_id', [
    ('21982806', variables.data_infor, 11383),
    ('21982807', variables.data_infor, 11384),
    ('21982808', variables.data_infor, 11385),
    ('21982809', variables.data_infor, 11386),
    ('21982810', variables.data_infor, 11387),
    ('21982811', variables.data_infor, 11388),
])
def test_response_infor(ilx_context, order_no, infor_data, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    headers = {'Authorization': ilx_context.ilx_infor_token}

    resp = requests.get(url=Utils.generate_url(ilx_context.ilx_data.ilx_infor_url, order_no=order_no), headers=headers)
    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_infor(Utils.get_data_order_infor(order_no, infor_data))

    print(response)
