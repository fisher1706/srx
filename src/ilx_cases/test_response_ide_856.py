# pylint: disable=C0305

import time
import pytest
import requests
from src.api.ilx.ilx_response import Response
from src.schemas.ilx_schemas import ValidatorIDE
from src.utilities.grnerate_data_test import GenerateIDE856
from src.utilities.ilx_utils import Utils


@pytest.mark.parametrize('number, test_type, testrail_case_id', [
    (1, 'pass', 10200),
    (1, 'fail', 10201)
])
def test_response_ide_856(ilx_context, number, test_type, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id

    Utils.cleaner(ilx_context.ilx_data.PATH_OUT)
    test_data = list()

    for _ in range(number):
        file_name, data = GenerateIDE856.generate_data_edi_856_rtf(test_type)
        Utils.create_rtf_file(ilx_context.ilx_data.PATH_OUT, file_name, data)
        test_data.append([v for k, v in data.items() if k in [3, 8, 15, 18]])

    Utils.upload_sftp_files(ilx_context.ilx_data.HOST_EDI856, ilx_context.USERNAME_EDI856, ilx_context.PASSWORD_EDI856,
                            ilx_context.ilx_data.PATH_OUT, ilx_context.ilx_data.INBOX_EDI856)

    time.sleep(5)

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

        print(response.__str__())
