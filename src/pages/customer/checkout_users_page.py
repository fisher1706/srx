from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.resources.tools import Tools
from src.resources.locator import Locator

class CheckoutUsersPage(CustomerPortalPage):
    checkout_user_body = {
        "firstName": None,
        "lastName": None,
        "fob": None,
        "passCode": None,
        "email": None,
        "phone": None
    }

    def create_checkout_user(self, checkout_user_body, first_group=False):
        self.wait_until_page_loaded()
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_add_button)
        for field in checkout_user_body.keys():
            self.input_by_name(field, checkout_user_body[field])
        if first_group:
            self.select_checkbox(Locator.xpath_checkbox)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows+1)

    def check_new_checkout_user(self, checkout_user_body, row):
        table_cells = {
            "Email": checkout_user_body["email"],
            "First Name": checkout_user_body["firstName"],
            "Last Name": checkout_user_body["lastName"],
            "FOB": checkout_user_body["fob"],
            "Passcode": checkout_user_body["passCode"],
            "Role": "Checkout User",
            "Phone": checkout_user_body["phone"]
        }
        for cell, value in table_cells.items():
            self.check_table_item_by_header(row, cell, value)

    def update_new_checkout_user(self, checkout_user_body, row, first_group=False):
        self.wait_until_page_loaded()
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, row))
        for field in checkout_user_body.keys():
            self.input_by_name(field, checkout_user_body[field])
        if first_group:
            self.select_checkbox(Locator.xpath_checkbox)
        self.click_xpath(Locator.xpath_submit_button)

    def delete_new_checkout_user(self, row):
        full_name = self.get_table_item_text_by_header("First Name", row)
        full_name += " " + self.get_table_item_text_by_header("Last Name", row)
        self.wait_until_page_loaded()
        self.get_element_by_xpath(Locator.xpath_by_count(Locator.xpath_table_row, row)+Locator.xpath_remove_button).click()
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def import_checkout_user(self, checkout_users):
        Tools.generate_csv("checkout_users.csv", checkout_users)
        self.import_csv(Locator.id_file_upload, "checkout_users.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()
