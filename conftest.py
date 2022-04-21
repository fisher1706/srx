import pytest
from glbl import LOG


pytest_plugins = [
    "src.fixtures.context_fixtures",
    "src.fixtures.ilx_context_fixtures",
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

    #SRX account for load testing
    parser.addoption('--load_distributor_email', action='store', default=None,
                     help="Enter email of distributor user")
    parser.addoption('--load_distributor_password', action='store', default=None,
                     help="Enter password of distributor user")
    parser.addoption('--load_customer_email', action='store', default=None,
                     help="Enter email of customer user")
    parser.addoption('--load_customer_password', action='store', default=None,
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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_exception_interact(report):
    LOG.error(f'Exception:\n{report.longreprtext}')
