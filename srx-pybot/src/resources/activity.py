from src.resources.data import Data
from src.resources.locators import Locators
from src.resources.logger import Logger
from src.resources.url import URL
from src.resources.variables import Variables
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys

class Activity():
    current_case = None
    def __init__(self):
        self.data = Data()
        self.locators = Locators()
        self.logger = Logger()
        self.url = URL()
        self.variables = Variables()
        if (len(sys.argv) == 1):
            self.configuration("firefox")
        elif (len(sys.argv) == 2):
            self.configuration(browser=sys.argv[1])

    def configuration(self, browser, wait=18):
        if (browser == 'firefox'):
            self.driver = webdriver.Firefox()
        elif (browser == 'firefox-headless' or browser == 'fhl'):
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
        else:
            pass
        self.driver.implicitly_wait(wait)

    def finish_activity(self):
        self.driver.close()