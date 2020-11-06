from src.pages.base_page import BasePage

class DistributorPortalPage(BasePage):
    def sidebar_account_status(self):
        self.click_xpath("//button[@data-testid='status-button']/..")

    def sidebar_users(self):
        self.click_id("sidebar-users-groups")

    def sidebar_warehouses(self):
        self.click_id("sidebar-warehouses")

    def sidebar_customers(self):
        self.click_id("sidebar-customers")

    def sidebar_catalog(self):
        self.click_id("sidebar-catalog")

    def sidebar_pricing(self):
        self.click_id("sidebar-pricing")

    def sidebar_settings(self):
        self.click_id("sidebar-settings")

    def sign_out(self):
        self.click_id("sidebar-sign_out")
    
    def sidebar_rfid(self):
        self.click_id("sidebar-rfid")

    def sidebar_serialization(self):
        self.click_id("sidebar-lot-serialization")

    def sidebar_hardware(self):
        self.click_id("sidebar-hardware")

    def sidebar_order_status(self):
        self.click_id("sidebar-order-status")

    def sidebar_support(self):
        self.click_id("sidebar-support")

    def distributor_sidebar_should_contain_email(self):
        self.get_element_by_xpath(f"//span[text()='{self.context.distributor_email}']")
