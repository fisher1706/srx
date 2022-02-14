from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class ShiptoPage(DistributorPortalPage):
    shipto_body = {
        "name": None,
        "number": None,
        "poNumber": None,
        "address.zipCode": None,
        "address.line1": None,
        "address.line2": None,
        "address.city": None,
        "state": None,
        "notes": None,
        "contactId": None
    }

    def follow_shipto_url(self):
        self.follow_url(f"{self.url.distributor_portal}/customers/{self.data.customer_id}#shiptos")

    def create_shipto(self, shipto_body):
        self.wait_until_page_loaded()
        self.open_last_page()
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), shipto_body.pop("state"))
        for field in shipto_body.keys():
            self.input_by_name(field, shipto_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.open_last_page()
        self.wait_until_page_loaded()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows+1)

    def check_last_shipto(self, shipto_body):
        self.open_last_page()
        table_cells = {
            "Shipto Number": shipto_body["number"],
            "Shipto Name": shipto_body["name"],
            "Address": [shipto_body["address.zipCode"], shipto_body["address.line1"], shipto_body["address.line2"], shipto_body["address.city"]],
            "PO Numbers": shipto_body["poNumber"]
        }
        for cell, value in table_cells.items():
            self.check_last_table_item_by_header(cell, value)

    def update_last_shipto(self, shipto_body, actions_pop_up=True):
        if actions_pop_up:
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_actions_button, self.get_table_rows_number()))
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_shipto_info_button, self.get_table_rows_number()))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), shipto_body.pop("state"))
        for field in shipto_body.keys():
            self.input_by_name(field, shipto_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_page_loaded()

    def delete_last_shipto(self, actions_pop_up=True):
        start_number_of_rows = self.get_table_rows_number()
        name = self.get_last_table_item_text_by_header("Shipto Number")
        if actions_pop_up:
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_actions_button, self.get_table_rows_number()))
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(name)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows-1)
