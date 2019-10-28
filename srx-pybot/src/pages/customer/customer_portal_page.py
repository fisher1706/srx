from src.pages.page import Page

class CustomerPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)

    def sidebar_users_and_groups(self):
        self.click_id("sidebar-users_and_groups")

    def sidebar_allocation_codes(self):
        self.click_id("sidebar-allocation_codes")

    def sign_out(self):
        self.click_id("sidebar-sign_out")