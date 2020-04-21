from src.pages.page import Page

class CustomerPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)

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
    
    def customer_sidebar_should_contain_email(self, email=None):
        if (email is None):
            email = self.variables.customer_email
        self.should_be_present_xpath(f"//span[text()='{email}']")
