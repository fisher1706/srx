from src.pages.page import Page

class DistributorPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)

    def sidebar_users(self):
        self.click_id("sidebar-distributor_users")

    def sidebar_warehouses(self):
        self.click_id("sidebar-warehouses")

    def sign_out(self):
        self.click_id("sidebar-sign_out")