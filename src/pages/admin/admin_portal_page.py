from src.pages.base_page import BasePage

class AdminPortalPage(BasePage):
    def admin_sidebar_should_contain_email(self):
        self.get_element_by_xpath(f"//span[text()='{self.context.admin_email}']")

    def sign_out(self):
        self.click_id("sidebar-sign-out")

    def sidebar_hardware(self):
        self.click_id("sidebar-hardware")

    def sidebar_universal_catalog(self):
        self.click_id("sidebar-universal-catalog")
    
    def sidebar_distributors(self):
        self.click_id("sidebar-distributors")
    
    def sidebar_fees(self):
        self.click_id("sidebar-fees")