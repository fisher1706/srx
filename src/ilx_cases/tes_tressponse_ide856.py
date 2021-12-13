import pytest
from src.utilities.ilx_utils import Utils
from src.utilities.grnerate_data_test import GenerateIDE856
from context import Context
from src.resources.local_credentials import LocalCredentials
import requests
import time
from src.api.ilx.ilx_response import Response
from src.schemas.ilx_schemas import ValidatorIDE
from src.resources.testrail import Testrail


@pytest.fixture(scope='function')
def generate_test_files(number, test_type):
    settings = LocalCredentials('ide_856')
    context = Context()

    context.testrail_run_id = ''

    Utils.cleaner(settings.PATH_RTF_OUT)

    test_data = list()

    for i in range(number):
        file_name, data = GenerateIDE856.generate_data_edi_856_rtf(test_type)
        Utils.create_rtf_file(settings.PATH_RTF_OUT, file_name, data)
        test_data.append([v for k, v in data.items() if k in [3, 8, 15, 18]])

    Utils.upload_sftp_files(settings.HOST_EDI856, settings.USERNAME_EDI856, settings.PASSWORD_EDI856,
                            settings.PATH_RTF_OUT, settings.INBOX_EDI856)

    return test_data, context, settings


@pytest.mark.parametrize('number, test_type', [
    (2, 'pass'),
    (2, 'fail')
])
def test_response_ide_856(number, test_type, generate_test_files):
    test_data = generate_test_files[0]
    context = generate_test_files[1]
    settings = generate_test_files[2]

    time.sleep(5)

    for data in test_data:
        case = data[1].split('*')[2]
        headers = {'Authorization': settings.token}
        resp = requests.get(url=Utils.generate_url(settings.url, case=case), headers=headers)
        response = Response(resp)
        if test_type == 'pass':
            response.validate_response_schema(ValidatorIDE)
            response.validate_response_edi(data)
        else:
            assert len(response.response_json) == 0

        print(response.__str__())

    context.testrail_comment = f"Test passed with data status - OK"

    testrail = Testrail(settings.testrail_email, settings.testrail_password)
    testrail.add_result_for_case(context.testrail_run_id, context.testrail_case_id,
                                 context.testrail_status_id, context.testrail_comment)
