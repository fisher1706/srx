from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class ShiptoPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.shipto_body = {
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
        self.follow_url(self.url.get_url_for_env("storeroomlogix.com/customers/"+self.variables.customer_id+"#shiptos", "distributor"))

    def create_shipto(self, shipto_body):
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), shipto_body.pop("state"))
        for field in shipto_body.keys():
            self.input_by_name(field, shipto_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(self.locators.xpath_table_row, start_number_of_rows+1)

    def check_last_shipto(self, shipto_body):
        self.open_last_page()
        table_cells = {
            "Shipto Number": shipto_body["number"],
            "Shipto Name": shipto_body["name"],
            "Address": [shipto_body["address.zipCode"], shipto_body["address.line1"], shipto_body["address.line2"], shipto_body["address.city"]],
            "PO Number": shipto_body["poNumber"]
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def update_last_shipto(self, shipto_body):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_shipto_info, self.get_table_rows_number()))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), shipto_body.pop("state"))
        for field in shipto_body.keys():
            self.input_by_name(field, shipto_body[field])
        self.click_xpath(self.locators.xpath_submit_button)

    def delete_last_shipto(self):
        start_number_of_rows = self.get_table_rows_number()
        name = self.get_last_table_item_text_by_header("Shipto Number")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_shipto, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.elements_count_should_be(self.locators.xpath_table_row, start_number_of_rows-1)