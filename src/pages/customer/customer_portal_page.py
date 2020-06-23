from src.pages.base_page import BasePage

class CustomerPortalPage(BasePage):
    def sidebar_users_and_groups(self):
        self.click_id("sidebar-users_and_groups")

    def sidebar_allocation_codes(self):
        self.click_id("sidebar-allocation_codes")

    def sidebar_activity_feed(self):
        self.click_id("sidebar-activity_feed")

    def sidebar_orders_and_quotes(self):
        self.click_id("sidebar-quoted_ordered_list")

    def sign_out(self):
        self.click_id("sidebar-sign_out")
    
    def sidebar_assets(self):
        self.click_id("sidebar-assets")
    
    def customer_sidebar_should_contain_email(self):
        self.get_element_by_xpath(f"//span[text()='{self.context.customer_email}']")
