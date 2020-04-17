from src.pages.page import Page
import time

class DistributorPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)

    def sidebar_account_status(self):
        self.click_xpath("//button[@data-testid='status-button']/..")

    def sidebar_users(self):
        self.click_id("sidebar-distributor_users")

    def sidebar_warehouses(self):
        self.click_id("sidebar-warehouses")

    def sidebar_customers(self):
        self.click_id("sidebar-customers")

    def sidebar_catalog(self):
        self.click_id("sidebar-catalog")

    def sidebar_pricing(self):
        self.click_id("sidebar-pricing")

    def sidebar_settings(self):
        self.click_id("sidebar--settings")

    def sign_out(self):
        self.click_id("sidebar-sign_out")
    
    def sidebar_rfid(self):
        self.click_id("sidebar-rfid")

    def sidebar_hardware(self):
        self.click_id("sidebar-claiming_hardware")

    def distributor_sidebar_should_contain_email(self):
        self.should_be_present_xpath(f"//span[text()='{self.variables.distributor_email}']")

    def get_authorization_token(self):
        cookies = self.driver.get_cookies()
        for cookies_dict in cookies:
            result = cookies_dict["name"].split(".")
            if ("idToken" in result):
                token = cookies_dict["value"]
                print(token)
                break
        return token