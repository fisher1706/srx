from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class DistributorCustomerUsersPage(DistributorPortalPage):
    def follow_customer_users_url(self, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        self.follow_url(f"{self.url.distributor_portal}/customers/{customer_id}#users")

    def follow_customer_settings_url(self, customer_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        self.follow_url(f"{self.url.distributor_portal}/customers/{customer_id}#settings")
