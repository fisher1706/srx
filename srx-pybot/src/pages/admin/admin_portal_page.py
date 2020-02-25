from src.pages.page import Page
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class AdminPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)
    
    def admin_sidebar_should_contain_email(self):
        self.should_be_present_xpath("//span[text()='"+self.variables.admin_email+"']")

    def sign_out(self):
        self.click_id("sidebar-sign-out")

    def sidebar_hardware(self):
        self.click_id("sidebar-hardware")

    def sidebar_universal_catalog(self):
        self.click_id("sidebar-universal-catalog")