import sys
import copy
import time
from collections import defaultdict
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from context import Context, SessionContext
from src.resources.url import URL
from src.resources.data import Data, SmokeData
from src.resources.logger import Logger
from src.resources.testrail import Testrail
from src.resources.tools import Tools

@pytest.fixture(scope="function")
def driver(request, session_context):
    browser_name = session_context.browser_name
    browser = None
    if browser_name == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1300,1000")
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        browser = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
    elif browser_name == "firefox":
        browser = webdriver.Firefox()
    elif browser_name == "chrome-headless":
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--enable-automation")
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        browser = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
    else:
        raise pytest.UsageError("--browser_name should be 'chrome', 'chrome-headless' or 'firefox'")
    browser.set_page_load_timeout(30)
    yield browser
    browser.quit()

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

    user_keys = Tools.get_yaml("user_keys.yml")

    for user_key in user_keys["keys"]:
        if session_context_object.credentials:
            session_context_object.__setattr__(user_key, request.config.getoption(user_key))
        else:
            user_local_values = Tools.get_yaml("user_local_values.yml")
            session_context_object.__setattr__(user_key, user_local_values[session_context_object.environment].get(user_key))

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
def srx_integration_context(context, request):
    context_object = context
    context_object.data = context_object.session_context.base_data

    #credentials
    context_object.admin_email = context_object.session_context.base_admin_email
    context_object.admin_password = context_object.session_context.base_admin_password
    context_object.distributor_email = context_object.session_context.ilx_distributor_email
    context_object.distributor_password = context_object.session_context.ilx_distributor_password
    context_object.customer_email = context_object.session_context.ilx_customer_email
    context_object.customer_password = context_object.session_context.ilx_customer_password

    yield context_object
    testrail(request, context_object)

@pytest.fixture(scope="function")
def load_context(context, request):
    context_object = context
    context_object.data = context_object.session_context.base_data

    #credentials
    context_object.distributor_email = context_object.session_context.load_distributor_email
    context_object.distributor_password = context_object.session_context.load_distributor_password
    context_object.customer_email = context_object.session_context.load_customer_email
    context_object.customer_password = context_object.session_context.load_customer_password

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
    if context.testrail_run_id is not None:
        if context.testrail_case_id is not None:
            if request.node.rep_setup.failed:
                context.testrail_status_id = 3
                context.testrail_comment = "[PYTEST] Unsuccessful attempt to run a test"
            elif request.node.rep_setup.passed:
                if request.node.rep_call.failed:
                    context.testrail_status_id = 5
                    context.testrail_comment = f"[PYTEST] Test failed \n{context.logger}\n{sys.last_value}"
                elif request.node.rep_call.passed:
                    if context.warnings_counter == 0:
                        context.testrail_status_id = 1
                        context.testrail_comment = "[PYTEST] Test passed"
                    elif context.warnings_counter > 0:
                        context.testrail_status_id = 6
                        context.testrail_comment = f"[PYTEST] Test passed with '{context.warnings_counter}' warnings\n{context.logger}"
                    else:
                        raise Exception(f"warnings_counter = '{context.warnings_counter}'")
                else:
                    raise Exception(f"Failed call: {request.node.rep_setup.failed}; Passed call: {request.node.rep_setup.passed}")
            else:
                raise Exception(f"Failed setup: {request.node.rep_setup.failed}; Passed setup: {request.node.rep_setup.passed}")

            testrail = Testrail(context.session_context.testrail_email, context.session_context.testrail_password)
            retries = 3
            for iteration in range(retries):
                time.sleep(iteration)
                response = testrail.add_result_for_case(context.testrail_run_id,
                                                        context.testrail_case_id,
                                                        context.testrail_status_id,
                                                        context.testrail_comment)
                if response.status_code == 500:
                    if iteration + 1 < retries:
                        context.logger.warning(f"Cannot connect to the testRail API. Next attempt after {iteration+1} seconds")
                    continue
                if response.status_code > 201 and response.status_code != 500:
                    error = str(response.content)
                    context.logger.error(f"TestRail API returned HTTP {response.status_code} ({error})", only_msg=True)
                    break
                else:
                    break
            else:
                context.logger.error("The result of the test has not been added to the TestRail")
        else:
            context.logger.warning("Testrail is not configured")

@pytest.fixture(scope="session")
def testrail_smoke_result(session_context):
    yield
    testrail_client = Testrail(session_context.testrail_email, session_context.testrail_password)
    tests = testrail_client.get_tests(session_context.smoke_data.smoke_testrail_run_id).json()["tests"]
    for test in tests:
        if test["status_id"] == 5:
            testrail_client.run_report(session_context.smoke_data.report_id)
            break
