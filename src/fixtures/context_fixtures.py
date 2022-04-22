import copy
import time
import os
from collections import defaultdict
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from context import Context, SessionContext
from glbl import Log, Var
from src.resources.url import URL
from src.resources.data import Data, SmokeData
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
    Log.clear()
    Var.clear()
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
    finalize(request, context_object)

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
    finalize(request, context_object)

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
    finalize(request, context_object)

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
    finalize(request, context_object)

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

def finalize(request, context):
    if context.testrail_run_id is not None:
        if context.testrail_case_id is not None:
            status = None
            comment = str()
            if request.node.rep_setup.failed:
                status = 3
                comment = "[PYTEST] Unsuccessful attempt to run a test"
            elif request.node.rep_setup.passed:
                if request.node.rep_call.failed:
                    status = 5
                    if context.session_context.screenshot and context.driver is not None:
                        path = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/screenshots/"
                        if not os.path.exists(path):
                            try:
                                os.mkdir(path)
                            except OSError:
                                Log.error("Creation of Screenshots directory is failed")
                        context.driver.save_screenshot(f"{path}{time.strftime('%Y.%m.%dT%H:%M:%S', time.localtime(time.time()))}.png")
                        Tools.generate_log(f"{path}{time.strftime('%Y.%m.%dT%H:%M:%S', time.localtime(time.time()))}.log", context.driver.get_log("performance"))
                        Log.info(f"URL: \n{context.driver.current_url}")
                        try:
                            Log.info(f"TEXT: \n{context.driver.find_element(By.XPATH, '//body').text}")
                        except:
                            Log.info("TEXT NOT FOUND")
                    comment = f"[PYTEST] Test failed\n{Log.text}"
                elif request.node.rep_call.passed:
                    if Var.teardown_error:
                        status = 6
                        comment = f"[PYTEST] Test passed, but teardown is failed\n{Log.text}"
                    else:
                        status = 1
                        comment = "[PYTEST] Test passed"

            testrail = Testrail(context.session_context.testrail_email, context.session_context.testrail_password)
            retries = 3
            for iteration in range(retries):
                time.sleep(iteration)
                response = testrail.add_result_for_case(context.testrail_run_id,
                                                        context.testrail_case_id,
                                                        status,
                                                        comment)
                if response.status_code == 500:
                    if iteration + 1 < retries:
                        Log.warning(f"Cannot connect to the testRail API. Next attempt after {iteration+1} seconds")
                    continue
                if response.status_code > 201 and response.status_code != 500:
                    error = str(response.content)
                    Log.error(f"TestRail API returned HTTP {response.status_code} ({error})")
                    break
                else:
                    break
            else:
                Log.error("The result of the test has not been added to the TestRail")
        else:
            Log.warning("Testrail is not configured")

@pytest.fixture(scope="session")
def testrail_smoke_result(session_context):
    yield
    testrail_client = Testrail(session_context.testrail_email, session_context.testrail_password)
    tests = testrail_client.get_tests(session_context.smoke_data.smoke_testrail_run_id).json()["tests"]
    for test in tests:
        if test["status_id"] in (5, 6):
            testrail_client.run_report(session_context.smoke_data.report_id)
            break
