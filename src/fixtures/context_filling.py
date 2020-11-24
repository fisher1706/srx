import pytest
from context import Context, SessionContext
from collections import defaultdict
from src.resources.url import URL
from src.resources.data import Data, SmokeData
from src.resources.logger import Logger
from src.resources.testrail import Testrail
import sys
import copy

@pytest.fixture(scope="session")
def session_context(request):
    session_context_object = SessionContext()

    #main args
    session_context_object.credentials = request.config.getoption("credentials")
    session_context_object.screenshot = request.config.getoption("screenshot")
    session_context_object.browser_name = request.config.getoption("browser_name")
    session_context_object.environment = request.config.getoption("environment")
    session_context_object.url = URL(session_context_object.environment)
    session_context_object.base_data = Data(session_context_object.environment)
    session_context_object.smoke_data = SmokeData(session_context_object.environment)

    #credentials
    if (session_context_object.credentials):
        #base credentials
        session_context_object.base_admin_email = request.config.getoption("base_admin_email")
        session_context_object.base_admin_password = request.config.getoption("base_admin_password")
        session_context_object.base_distributor_email = request.config.getoption("base_distributor_email")
        session_context_object.base_distributor_password = request.config.getoption("base_distributor_password")
        session_context_object.base_customer_email = request.config.getoption("base_customer_email")
        session_context_object.base_customer_password = request.config.getoption("base_customer_password")
        session_context_object.base_checkout_group_email = request.config.getoption("base_checkout_group_email")
        session_context_object.base_checkout_group_password = request.config.getoption("base_checkout_group_password")

        #smoke credentials
        session_context_object.smoke_distributor_email = request.config.getoption("smoke_distributor_email")
        session_context_object.smoke_distributor_password = request.config.getoption("smoke_distributor_password")
        session_context_object.smoke_customer_email = request.config.getoption("smoke_customer_email")
        session_context_object.smoke_customer_password = request.config.getoption("smoke_customer_password")

        #permission credentials
        session_context_object.permission_distributor_email = request.config.getoption("permission_distributor_email")
        session_context_object.permission_distributor_password = request.config.getoption("permission_distributor_password")
        session_context_object.permission_customer_email = request.config.getoption("permission_customer_email")
        session_context_object.permission_customer_password = request.config.getoption("permission_customer_password")

        #testrail credentials
        session_context_object.testrail_email = request.config.getoption("testrail_email")
        session_context_object.testrail_password = request.config.getoption("testrail_password")

        #cognito credentials
        session_context_object.cognito_user_pool_id = request.config.getoption("cognito_user_pool_id")
        session_context_object.cognito_client_id = request.config.getoption("cognito_client_id")
        session_context_object.cognito_mobile_client_id = request.config.getoption("cognito_mobile_client_id")
        session_context_object.cognito_checkout_client_id = request.config.getoption("cognito_checkout_client_id")

    elif (not session_context_object.credentials):
        from src.resources.local_credentials import LocalCredentials
        creds = LocalCredentials(session_context_object.environment)

        #base credentials
        session_context_object.base_admin_email = creds.base_admin_email
        session_context_object.base_admin_password = creds.base_admin_password
        session_context_object.base_distributor_email = creds.base_distributor_email
        session_context_object.base_distributor_password = creds.base_distributor_password
        session_context_object.base_customer_email = creds.base_customer_email
        session_context_object.base_customer_password = creds.base_customer_password
        session_context_object.base_checkout_group_email = creds.base_checkout_group_email
        session_context_object.base_checkout_group_password = creds.base_checkout_group_password

        #smoke credentials
        session_context_object.smoke_distributor_email = creds.smoke_distributor_email
        session_context_object.smoke_distributor_password = creds.smoke_distributor_password
        session_context_object.smoke_customer_email = creds.smoke_customer_email
        session_context_object.smoke_customer_password = creds.smoke_customer_password

        #permission credentials
        session_context_object.permission_distributor_email = creds.permission_distributor_email
        session_context_object.permission_distributor_password = creds.permission_distributor_password
        session_context_object.permission_customer_email = creds.permission_customer_email
        session_context_object.permission_customer_password = creds.permission_customer_password

        #testrail credentials
        session_context_object.testrail_email = creds.testrail_email
        session_context_object.testrail_password = creds.testrail_password

        #cognito credentials
        session_context_object.cognito_user_pool_id = creds.USER_POOL_ID
        session_context_object.cognito_client_id = creds.CLIENT_ID
        session_context_object.cognito_mobile_client_id = creds.MOBILE_CLIENT_ID
        session_context_object.cognito_checkout_client_id = creds.CHECKOUT_CLIENT_ID

    return session_context_object

@pytest.fixture(scope="function")
def context(session_context):
    context_object = Context()
    context_object.dynamic_context = defaultdict(list)
    context_object.session_context = session_context
    context_object.logger = Logger(context_object)
    return context_object

@pytest.fixture(scope="function")
def base_context(context, request):
    context_object = context
    context_object.data = context_object.session_context.base_data

    #credentials
    context_object.admin_email = context_object.session_context.base_admin_email
    context_object.admin_password = context_object.session_context.base_admin_password
    context_object.distributor_email = context_object.session_context.base_distributor_email
    context_object.distributor_password = context_object.session_context.base_distributor_password
    context_object.customer_email = context_object.session_context.base_customer_email
    context_object.customer_password = context_object.session_context.base_customer_password
    context_object.checkout_group_email = context_object.session_context.base_checkout_group_email
    context_object.checkout_group_password = context_object.session_context.base_checkout_group_password

    yield context_object
    testrail(request, context_object)

@pytest.fixture(scope="function")
def smoke_context(context, request, testrail_smoke_result):
    context_object = context
    context_object.data = context_object.session_context.smoke_data

    #credentials
    context_object.distributor_email = context_object.session_context.smoke_distributor_email
    context_object.distributor_password = context_object.session_context.smoke_distributor_password
    context_object.customer_email = context_object.session_context.smoke_customer_email
    context_object.customer_password = context_object.session_context.smoke_customer_password

    yield context_object
    testrail(request, context_object)

@pytest.fixture(scope="function")
def permission_context(context, request):
    context_object = copy.copy(context)
    context_object.data = context_object.session_context.base_data

    #credentials
    context_object.distributor_email = context_object.session_context.permission_distributor_email
    context_object.distributor_password = context_object.session_context.permission_distributor_password
    context_object.customer_email = context_object.session_context.permission_customer_email
    context_object.customer_password = context_object.session_context.permission_customer_password
    return context_object

def testrail(request, context):
    if (context.testrail_case_id is not None):
        if (request.node.rep_setup.failed):
            context.testrail_status_id = 3
            context.testrail_comment = "[PYTEST] Unsuccessful attempt to run a test"
        elif (request.node.rep_setup.passed):
            if (request.node.rep_call.failed):
                context.testrail_status_id = 5
                context.testrail_comment = f"[PYTEST] Test failed \n{context.logger}\n{sys.last_value}"
            elif (request.node.rep_call.passed):
                if (context.warnings_counter == 0):
                    context.testrail_status_id = 1
                    context.testrail_comment = "[PYTEST] Test passed"
                elif (context.warnings_counter > 0):
                    context.testrail_status_id = 6
                    context.testrail_comment = f"[PYTEST] Test passed with '{context.warnings_counter}' warnings\n{context.logger}"
                else:
                    raise Exception(f"warnings_counter = '{context.warnings_counter}'")
            else:
                raise Exception(f"Failed call: {request.node.rep_setup.failed}; Passed call: {request.node.rep_setup.passed}")
        else:
            raise Exception(f"Failed setup: {request.node.rep_setup.failed}; Passed setup: {request.node.rep_setup.passed}")

        testrail = Testrail(context.session_context.testrail_email, context.session_context.testrail_password)
        testrail.add_result_for_case(context.testrail_run_id,
                                    context.testrail_case_id,
                                    context.testrail_status_id,
                                    context.testrail_comment)
    else:
        context.logger.warning("Testrail is not configured")

@pytest.fixture(scope="session")
def testrail_smoke_result(session_context):
    yield
    testrail_client = Testrail(session_context.testrail_email, session_context.testrail_password)
    tests = testrail_client.get_tests(session_context.smoke_data.smoke_testrail_run_id)
    for test in tests:
        if (test["status_id"] == 5):
            testrail_client.run_report(session_context.smoke_data.report_id)
            break