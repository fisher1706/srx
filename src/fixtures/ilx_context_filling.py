import sys
import time
import pytest
from ilx_context import IlxContext, IlxSessionContext
from src.resources.ilx_data import IlxData
from src.resources.testrail import Testrail


@pytest.fixture(scope="session")
def ilx_session_context(request):
    ilx_session_context_object = IlxSessionContext()

    # main args
    ilx_session_context_object.ilx_credentials = request.config.getoption("ilx_credentials")
    ilx_session_context_object.ilx_environment = request.config.getoption("ilx_environment")
    ilx_session_context_object.ilx_browser_name = request.config.getoption("browser_name")
    ilx_session_context_object.ilx_base_data = IlxData(ilx_session_context_object.ilx_environment)

    # credentials
    if ilx_session_context_object.ilx_credentials:
        # base credentials
        ilx_session_context_object.ilx_testrail_email = request.config.getoption ("testrail_email")
        ilx_session_context_object.ilx_testrail_password = request.config.getoption ("testrail_password")

        ilx_session_context_object.ilx_auth_token = request.config.getoption("ilx_auth_token")
        ilx_session_context_object.ilx_infor_token = request.config.getoption("ilx_infor_token")

        ilx_session_context_object.ilx_wmi_token = request.config.getoption("ilx_wmi_token")

    elif not ilx_session_context_object.ilx_credentials:
        from src.resources.ilx_local_credentials import IlxLocalCredentials
        creds = IlxLocalCredentials(ilx_session_context_object.ilx_environment)

        # base credentials
        ilx_session_context_object.ilx_testrail_email = creds.ilx_testrail_email
        ilx_session_context_object.ilx_testrail_password = creds.ilx_testrail_password

        ilx_session_context_object.ilx_auth_token = creds.ilx_auth_token

        ilx_session_context_object.edi_856_auth_token = creds.edi_856_auth_token
        ilx_session_context_object.user_name_edi_856 = creds.user_name_edi_856
        ilx_session_context_object.password_edi_856 = creds.password_edi_856

        ilx_session_context_object.ilx_infor_token = creds.ilx_infor_token

        ilx_session_context_object.ilx_url = creds.ilx_url
        ilx_session_context_object.ilx_email = creds.ilx_email
        ilx_session_context_object.ilx_password = creds.ilx_password

        ilx_session_context_object.ilx_wmi_token = creds.ilx_wmi_token

    return ilx_session_context_object


@pytest.fixture(scope="function")
def ilx_context(ilx_session_context, request):
    ilx_context_object = IlxContext()

    ilx_context_object.ilx_session_context = ilx_session_context
    ilx_context_object.ilx_data = ilx_context_object.ilx_session_context.ilx_base_data

    ilx_context_object.ilx_testrail_run_id = 282

    ilx_context_object.ilx_auth_token = ilx_session_context.ilx_auth_token

    ilx_context_object.edi_856_auth_token = ilx_session_context.edi_856_auth_token
    ilx_context_object.password_edi_856 = ilx_session_context.password_edi_856
    ilx_context_object.user_name_edi_856 = ilx_session_context.user_name_edi_856

    ilx_context_object.ilx_infor_token = ilx_session_context.ilx_infor_token

    ilx_context_object.ilx_email = ilx_session_context.ilx_email
    ilx_context_object.ilx_password = ilx_session_context.ilx_password

    ilx_context_object.ilx_wmi_token = ilx_session_context.ilx_wmi_token

    yield ilx_context_object
    testrail(request, ilx_context_object)


def testrail(request, ilx_context):
    if ilx_context.ilx_testrail_case_id is not None:
        if request.node.rep_setup.failed:
            ilx_context.ilx_testrail_status_id = 3
            ilx_context.ilx_testrail_comment = "[PYTEST] Unsuccessful attempt to run a test"
        elif request.node.rep_setup.passed:
            if request.node.rep_call.failed:
                ilx_context.ilx_testrail_status_id = 5
                ilx_context.ilx_testrail_comment = f"[PYTEST] Test failed \n{sys.last_value}"
            elif request.node.rep_call.passed:
                ilx_context.ilx_testrail_status_id = 1
                ilx_context.ilx_testrail_comment = "[PYTEST] Test passed"
            else:
                raise Exception(
                    f"Failed call: {request.node.rep_setup.failed}; Passed call: {request.node.rep_setup.passed}")
        else:
            raise Exception(
                f"Failed setup: {request.node.rep_setup.failed}; Passed setup: {request.node.rep_setup.passed}")

        testrail = Testrail(ilx_context.ilx_session_context.ilx_testrail_email,
                            ilx_context.ilx_session_context.ilx_testrail_password)
        retries = 3
        for iteration in range(retries):
            time.sleep(iteration)
            response = testrail.add_result_for_case(ilx_context.ilx_testrail_run_id,
                                                    ilx_context.ilx_testrail_case_id,
                                                    ilx_context.ilx_testrail_status_id,
                                                    ilx_context.ilx_testrail_comment)
            if response.status_code == 500:
                if iteration + 1 < retries:
                    print(f"Cannot connect to the testRail API. Next attempt after {iteration + 1} seconds")
                continue
            if response.status_code > 201 and response.status_code != 500:
                error = str(response.content)
                print(f"TestRail API returned HTTP {response.status_code} ({error})")
                break
            else:
                break
        else:
            print("The result of the test has not been added to the TestRail")
    else:
        print("Testrail is not configured")
