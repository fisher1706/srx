import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

pytest_plugins = [
   "src.fixtures.context_filling",
   "src.fixtures.api_teardowns"
]

def pytest_addoption(parser):
    #main args
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: 'chrome', 'chrome-headless' or 'firefox'")
    parser.addoption('--environment', action='store', default='qa',
                     help="Choose environment: 'dev', 'qa', 'staging', 'prod'")
    parser.addoption('--credentials', action='store', nargs='?', const=True, default=False,
                    help="If selected, credentials will be retrieved ONLY from the command line")

    #credentials
    parser.addoption('--admin_email', action='store', default=None,
                     help="Enter email of admin user")
    parser.addoption('--admin_password', action='store', default=None,
                     help="Enter password of admin user")
    parser.addoption('--distributor_email', action='store', default=None,
                     help="Enter email of distributor user")
    parser.addoption('--distributor_password', action='store', default=None,
                     help="Enter password of distributor user")
    parser.addoption('--customer_email', action='store', default=None,
                     help="Enter email of customer user")
    parser.addoption('--customer_password', action='store', default=None,
                     help="Enter password of customer user")
    parser.addoption('--checkout_group_email', action='store', default=None,
                     help="Enter email of checkout group")
    parser.addoption('--checkout_group_password', action='store', default=None,
                     help="Enter password of checkout_group")
    parser.addoption('--testrail_email', action='store', default=None,
                     help="Enter email of testrail account")
    parser.addoption('--cognito_user_pool_id', action='store', default=None,
                     help="Enter cognito_user_pool_id")
    parser.addoption('--cognito_client_id', action='store', default=None,
                     help="Enter cognito_client_id")
    parser.addoption('--cognito_checkout_client_id', action='store', default=None,
                     help="Enter cognito_checkout_client_id")
    parser.addoption('--cognito_client_secret', action='store', default=None,
                     help="Enter cognito_client_secret")
    parser.addoption('--testrail_password', action='store', default=None,
                     help="Enter password of testrail account")

@pytest.fixture(scope="function")
def driver(request, session_context):
    browser_name = session_context.browser_name
    driver = None
    if browser_name == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1300,1000")
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "chrome-headless":
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1300,1000")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        raise pytest.UsageError("--browser_name should be 'chrome' or 'firefox'")
    driver.set_page_load_timeout(20)
    yield driver
    driver.quit()

@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    rep = __multicall__.execute()
    setattr(item, "rep_" + rep.when, rep)
    return rep