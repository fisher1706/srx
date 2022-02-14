import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

pytest_plugins = [
    "src.fixtures.context_filling",
    "src.fixtures.ilx_context_filling",
    "src.fixtures.high_level_contexts",
    "src.fixtures.ilx_high_level_contexts",
    "src.fixtures.api_teardowns",
    "src.fixtures.presets"
]

def pytest_addoption(parser):
    #main args
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: 'chrome', 'chrome-headless' or 'firefox'")
    parser.addoption('--environment', action='store', default='qa',
                     help="Choose environment: 'dev', 'qa', 'staging', 'prod'")
    parser.addoption('--credentials', action='store', nargs='?', const=True, default=False,
                     help="If selected, credentials will be retrieved ONLY from the command line")
    parser.addoption('--screenshot', action='store', nargs='?', const=True, default=False,
                     help="If selected, screenshot will be created when error occurs")

    #base credentials
    parser.addoption('--base_admin_email', action='store', default=None,
                     help="Enter email of admin user")
    parser.addoption('--base_admin_password', action='store', default=None,
                     help="Enter password of admin user")
    parser.addoption('--base_distributor_email', action='store', default=None,
                     help="Enter email of distributor user")
    parser.addoption('--base_distributor_password', action='store', default=None,
                     help="Enter password of distributor user")
    parser.addoption('--base_customer_email', action='store', default=None,
                     help="Enter email of customer user")
    parser.addoption('--base_customer_password', action='store', default=None,
                     help="Enter password of customer user")
    parser.addoption('--base_checkout_group_email', action='store', default=None,
                     help="Enter email of checkout group")
    parser.addoption('--base_checkout_group_password', action='store', default=None,
                     help="Enter password of checkout_group")

    #smoke credentials
    parser.addoption('--smoke_distributor_email', action='store', default=None,
                     help="Enter email of distributor user")
    parser.addoption('--smoke_distributor_password', action='store', default=None,
                     help="Enter password of distributor user")
    parser.addoption('--smoke_customer_email', action='store', default=None,
                     help="Enter email of customer user")
    parser.addoption('--smoke_customer_password', action='store', default=None,
                     help="Enter password of customer user")

    #permission credentials
    parser.addoption('--permission_distributor_email', action='store', default=None,
                     help="Enter email of distributor user")
    parser.addoption('--permission_distributor_password', action='store', default=None,
                     help="Enter password of distributor user")
    parser.addoption('--permission_customer_email', action='store', default=None,
                     help="Enter email of customer user")
    parser.addoption('--permission_customer_password', action='store', default=None,
                     help="Enter password of customer user")

    #SRX account for ILX mocks credentials
    parser.addoption('--ilx_distributor_email', action='store', default=None,
                     help="Enter email of distributor user")
    parser.addoption('--ilx_distributor_password', action='store', default=None,
                     help="Enter password of distributor user")
    parser.addoption('--ilx_customer_email', action='store', default=None,
                     help="Enter email of customer user")
    parser.addoption('--ilx_customer_password', action='store', default=None,
                     help="Enter password of customer user")

    #testrail
    parser.addoption('--testrail_email', action='store', default=None,
                     help="Enter email of testrail account")
    parser.addoption('--testrail_password', action='store', default=None,
                     help="Enter password of testrail account")

    #cognito
    parser.addoption('--cognito_user_pool_id', action='store', default=None,
                     help="Enter cognito_user_pool_id")
    parser.addoption('--cognito_client_id', action='store', default=None,
                     help="Enter cognito_client_id")
    parser.addoption('--cognito_checkout_client_id', action='store', default=None,
                     help="Enter cognito_checkout_client_id")
    parser.addoption('--cognito_mobile_client_id', action='store', default=None,
                     help="Enter cognito_mobile_client_id")

    #ilx
    parser.addoption('--ilx_environment', action='store', default='qa',
                     help="Choose environment: 'dev', 'qa', 'prod'")
    parser.addoption('--ilx_credentials', action='store', nargs='?', const=True, default=False,
                     help="If selected, credentials will be retrieved ONLY from the command line")

    parser.addoption('--ilx_auth_token', action='store', default=None,
                     help="Enter ilx_auth_token")

    parser.addoption('--edi_856_auth_token', action='store', default=None,
                     help="Enter edi_856_auth_token")
    parser.addoption('--user_name_edi_856', action='store', default=None,
                     help="Enter user_name_edi_856")
    parser.addoption('--password_edi_856', action='store', default=None,
                     help="Enter password_edi_856")

    parser.addoption ('--ilx_infor_token', action='store', default='qa',
                      help="Enter ilx_infor_token")

    parser.addoption ('--ilx_wmi_token', action='store', default='qa',
                      help="Enter ilx_wmi_token")

    parser.addoption ('--ilx_billing_token', action='store', default='qa',
                      help="Enter ilx_billing_token")


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

@pytest.fixture(scope="function")
def driver_ilx(request, ilx_session_context):
    browser_name = ilx_session_context.ilx_browser_name
    browser = None
    if browser_name == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        browser = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        if request.cls is not None:
            request.cls.browser = browser
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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
