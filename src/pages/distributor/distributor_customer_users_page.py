from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class DistributorCustomerUsersPage(DistributorPortalPage):
    def create_customer_user(self, email):
        self.click_id(Locator.id_add_button)
        self.input_by_name(field, email)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_last_customer_user(self, customer_user_body):
        self.open_last_page()
        for cell in customer_user_body.keys():
            self.check_last_table_item_by_header(cell, customer_user_body[cell])

    def follow_customer_users_url(self, customer_id=None):
        if (customer_id is None):
            customer_id = self.data.customer_id
        self.follow_url(self.url.get_url_for_env(f"storeroomlogix.com/customers/{customer_id}#users", "distributor"), hide_intercom=True)