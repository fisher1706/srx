from src.resources.locators import Locators
from src.resources.logger import Logger
from src.resources.url import URL
from selenium import webdriver
from src.resources.variables import Variables
from selenium.webdriver.firefox.options import Options
import argparse

class Activity():
    def __init__(self, api_test=False, smoke=None):
        self.api_test = api_test
        self.smoke = smoke
        self.get_args()
        self.credentials_config()
        self.portal_credentials = {
            "admin_email": self.admin_email,
            "admin_password": self.admin_password,
            "distributor_email": self.distributor_email,
            "distributor_password": self.distributor_password,
            "customer_email": self.customer_email,
            "customer_password": self.customer_password,
            "checkout_group_email": self.checkout_group_email,
            "checkout_group_password": self.checkout_group_password
        }
        self.locators = Locators()
        self.logger = Logger()
        self.variables = Variables(self.arg_environment, self.portal_credentials, smoke)
        self.url = URL(self.arg_environment)
        self.logger.expected_error_series = self.variables.expected_error_series
        self.run_number = None

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--browser", "-b", help="Set browser: "+
                            "[ff] - Firefox; "+
                            "[ffhl] - Firefox headless; "+
                            "[chrome] - Chrome")
        parser.add_argument("--environment", "-e", help="Set environment : [dev]; [qa]; [staging]")
        parser.add_argument("--USER_POOL_ID", "-p", help="Set ID of Cognito User Pool")
        parser.add_argument("--CLIENT_ID", "-i", help="Set ID of Cognito Client")
        parser.add_argument("--CLIENT_SECRET", "-s", help="Set Secret Key of Cognito Client")
        parser.add_argument("--CHECKOUT_CLIENT_ID", "-ch", help="Set ID of Cognito Checkout Client")
        parser.add_argument("--email_address", "-ea", help="Set email address of inbox email")
        parser.add_argument("--email_password", "-ep", help="Set password of inbox email")
        parser.add_argument("--testrail_email", "-te", help="Set email address of testrail account")
        parser.add_argument("--testrail_password", "-tp", help="Set password of testrail account")
        parser.add_argument("--admin_email", "-ae", help="Set email address of admin portal")
        parser.add_argument("--admin_password", "-ap", help="Set password of admin portal")
        parser.add_argument("--distributor_email", "-de", help="Set email address of distributor portal")
        parser.add_argument("--distributor_password", "-dp", help="Set password of distributor portal")
        parser.add_argument("--customer_email", "-ce", help="Set email address of customer portal")
        parser.add_argument("--customer_password", "-cp", help="Set password of customer portal")
        parser.add_argument("--checkout_group_email", "-che", help="Set email address of checkout group")
        parser.add_argument("--checkout_group_password", "-chp", help="Set password of checkout group")
        parser.add_argument("--credentials", "-c", default=False, nargs='?', const=True, help="If present, credentials will be taken from the command line")
        args = parser.parse_args()
        self.arg_browser = args.browser
        self.arg_environment = args.environment
        self.USER_POOL_ID = args.USER_POOL_ID
        self.CLIENT_ID = args.CLIENT_ID 
        self.CLIENT_SECRET = args.CLIENT_SECRET
        self.CHECKOUT_CLIENT_ID = args.CHECKOUT_CLIENT_ID 
        self.email_address = args.email_address
        self.email_password = args.email_password
        self.testrail_email = args.testrail_email
        self.testrail_password = args.testrail_password
        self.remote_credentials = args.credentials
        self.admin_email = args.admin_email
        self.admin_password = args.admin_password
        self.distributor_email = args.distributor_email
        self.distributor_password = args.distributor_password
        self.customer_email = args.customer_email
        self.customer_password = args.customer_password
        self.checkout_group_email = args.checkout_group_email
        self.checkout_group_password = args.checkout_group_password

    def browser_config(self):
        if (self.api_test == False):
            browser = self.arg_browser
            if (browser == 'ff' or browser is None):
                self.driver = webdriver.Firefox()
            elif (browser == 'ffhl'):
                options = Options()
                options.headless = True
                self.driver = webdriver.Firefox(options=options)
            elif (browser == 'chrome'):
                self.driver = webdriver.Chrome()
            else:
                pass
            self.driver.implicitly_wait(self.variables.default_wait)

    def credentials_config(self):
        if (self.remote_credentials == False):
            from src.resources.local_credentials import LocalCredentials
            local_credentials = LocalCredentials(self.arg_environment, self.smoke)
            if (self.USER_POOL_ID is None):
                self.USER_POOL_ID = local_credentials.USER_POOL_ID
            if (self.CLIENT_ID is None):
                self.CLIENT_ID = local_credentials.CLIENT_ID
            if (self.CHECKOUT_CLIENT_ID is None):
                self.CHECKOUT_CLIENT_ID = local_credentials.CHECKOUT_CLIENT_ID
            if (self.CLIENT_SECRET is None):
                self.CLIENT_SECRET = local_credentials.CLIENT_SECRET
            if (self.email_address is None):
                self.email_address = local_credentials.email_address
            if (self.email_password is None):
                self.email_password = local_credentials.email_password
            if (self.testrail_email is None):
                self.testrail_email = local_credentials.testrail_email
            if (self.testrail_password is None):
                self.testrail_password = local_credentials.testrail_password
            if (self.admin_email is None):
                self.admin_email = local_credentials.admin_email
            if (self.admin_password is None):
                self.admin_password = local_credentials.admin_password
            if (self.distributor_email is None):
                self.distributor_email = local_credentials.distributor_email
            if (self.distributor_password is None):
                self.distributor_password = local_credentials.distributor_password
            if (self.customer_email is None):
                self.customer_email = local_credentials.customer_email
            if (self.customer_password is None):
                self.customer_password = local_credentials.customer_password
            if (self.checkout_group_email is None):
                self.checkout_group_email = local_credentials.checkout_group_email
            if (self.checkout_group_password is None):
                self.checkout_group_password = local_credentials.checkout_group_password