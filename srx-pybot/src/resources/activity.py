from src.resources.data import Data
from src.resources.locators import Locators
from src.resources.logger import Logger
from src.resources.url import URL
from src.resources.variables import Variables
from selenium import webdriver

class Activity():
    def __init__(self):
        self.data = Data()
        self.locators = Locators()
        self.logger = Logger()
        self.url = URL()
        self.variables = Variables()
        self.configuration()

    def configuration(self, browser='firefox', wait=20):
        if (browser=='firefox'):
            self.driver = webdriver.Firefox()
        else:
            pass
        self.driver.implicitly_wait(wait)

    def finish_activity(self):
        self.driver.close()