from src.resources.locators import Locators
from src.resources.logger import Logger
from src.resources.url import URL
from src.resources.variables import Variables
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import argparse

class Activity():
    
    def __init__(self):
        self.arg_browser, self.arg_environment, self.USER_POOL_ID, self.CLIENT_ID, self.CLIENT_SECRET = self.get_args()
        self.locators = Locators()
        self.logger = Logger()
        self.variables = Variables(self.arg_environment)
        self.url = URL(self.arg_environment)
        self.logger.expected_error_series = self.variables.expected_error_series
        self.browser_config(self.arg_browser)
        self.cognito_credentials_config(self.USER_POOL_ID, self.CLIENT_ID, self.CLIENT_SECRET)

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--browser", "-b", help="Set browser: "+
                            "[ff] - Firefox; "+
                            "[ffhl] - Firefox headless "+
                            "[chrome] - Chrome")
        parser.add_argument("--environment", "-e", help="Set environment : [dev]; [staging]")
        parser.add_argument("--USER_POOL_ID", "-p", help="Set ID of Cognito User Pool")
        parser.add_argument("--CLIENT_ID", "-i", help="Set ID of Cognito Client")
        parser.add_argument("--CLIENT_SECRET", "-s", help="Set Secret Key of Cognito Client")
        args = parser.parse_args()
        return args.browser, args.environment, args.USER_POOL_ID, args.CLIENT_ID, args.CLIENT_SECRET

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

    def cognito_credentials_config(self, USER_POOL_ID, CLIENT_ID, CLIENT_SECRET):
        if (USER_POOL_ID is None or CLIENT_ID is None or CLIENT_SECRET is None):
            from src.resources.local_cognito_credentials import local_cognito_credentials
            self.USER_POOL_ID, self.CLIENT_ID, self.CLIENT_SECRET = local_cognito_credentials()

    def finish_activity(self):
        self.driver.close()