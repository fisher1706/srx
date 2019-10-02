from src.pages.page import Page

class DistributorPortalPage(Page):
    def __init__(self, activity):
        super().__init__(activity)

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

    def sign_out(self):
        self.click_id("sidebar-sign_out")