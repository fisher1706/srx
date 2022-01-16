import time
import pytest
import requests
from src.api.ilx.ilx_response import Response
from src.schemas.ilx_schemas import ValidatorIDE
from src.utilities.grnerate_data_test import GenerateInforOrderStatusV2 as Infor
from src.utilities.ilx_utils import Utils


@pytest.mark.parametrize('number, test_type, testrail_case_id', [
    (1, 'pass', 10200),
    (1, 'fail', 10201)
])
def test_response_ide_856(ilx_context, number, test_type, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id



    for data in test_data:
        case = data[1].split('*')[2]
        headers = {'Authorization': ilx_context.edi_856_auth_token}

        resp = requests.get(url=Utils.generate_url(ilx_context.ilx_data.edi_856_url, case=case), headers=headers)

        response = Response(resp)
        if test_type == 'pass':
            response.validate_response_schema(ValidatorIDE)
            response.validate_response_edi(data)
        else:
            assert len(response.response_json) == 0

        print(response)
