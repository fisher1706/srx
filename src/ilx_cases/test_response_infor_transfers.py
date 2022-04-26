import pytest
import requests

from src.api.ilx.ilx_response import Response
from src.erp_emulator.erp_ilx import variables
from src.schemas.ilx_schemas import ValidatorInforTransfers


@pytest.mark.parametrize('data_infor_transfers, testrail_case_id', [
    (variables.data_infor_transfers, 12521),
])
def test_response_infor_transfers(ilx_context, data_infor_transfers, testrail_case_id):
    ilx_context.ilx_testrail_case_id = testrail_case_id
    headers = {'Authorization': ilx_context.ilx_qa_token}

    resp = requests.get(url=ilx_context.ilx_data.ilx_infor_transfers_url, headers=headers)

    response = Response(resp)
    response.assert_response_status(200)
    response.validate_response_schema(ValidatorInforTransfers)
    response.validate_response_infor_transfers(data_infor_transfers)

    print(response)
