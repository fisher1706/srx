from src.resources.locators import Locators
from src.resources.logger import Logger
from src.resources.url import URL
from src.resources.variables import Variables
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import argparse

class Activity():
    def __init__(self, api_test=False):
        self.get_args()
        self.locators = Locators()
        self.logger = Logger()
        self.variables = Variables(self.arg_environment)
        self.url = URL(self.arg_environment)
        self.logger.expected_error_series = self.variables.expected_error_series
        self.browser_config(self.arg_browser)
        self.credentials_config()

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--browser", "-b", help="Set browser: "+
                            "[ff] - Firefox; "+
                            "[ffhl] - Firefox headless "+
                            "[chrome] - Chrome")
        parser.add_argument("--environment", "-e", help="Set environment : [qa]; [staging]")
        parser.add_argument("--USER_POOL_ID", "-p", help="Set ID of Cognito User Pool")
        parser.add_argument("--CLIENT_ID", "-i", help="Set ID of Cognito Client")
        parser.add_argument("--CLIENT_SECRET", "-s", help="Set Secret Key of Cognito Client")
        parser.add_argument("--email_address", "-ea", help="Set email address of inbox email")
        parser.add_argument("--email_password", "-ep", help="Set password of inbox email")
        parser.add_argument("--testrail_email", "-te", help="Set email address of testrail account")
        parser.add_argument("--testrail_password", "-tp", help="Set password of testrail account")
        parser.add_argument("--remotely", "-r", default=False, nargs='?', const=True, help="If present, credentials will be taken from the buildspec")
        args = parser.parse_args()
        self.arg_browser = args.browser
        self.arg_environment = args.environment
        self.USER_POOL_ID = args.USER_POOL_ID
        self.CLIENT_ID = args.CLIENT_ID 
        self.CLIENT_SECRET = args.CLIENT_SECRET
        self.email_address = args.email_address
        self.email_password = args.email_password
        self.testrail_email = args.testrail_email
        self.testrail_password = args.testrail_password
        self.remote_credentials = args.remotely

    def browser_config(self, browser):
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
            local_credentials = LocalCredentials()
            if (self.USER_POOL_ID is None):
                self.USER_POOL_ID = local_credentials.USER_POOL_ID
            if (self.CLIENT_ID is None):
                self.CLIENT_ID = local_credentials.CLIENT_ID
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

    def finish_activity(self):
        self.driver.close()