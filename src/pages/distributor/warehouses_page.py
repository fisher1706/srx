from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class WarehousesPage(DistributorPortalPage):
    warehouse_body = {
        "name": None,
        "number": None,
        "address.line1": None,
        "address.line2": None,
        "address.city": None,
        "address.zipCode": None,
        "state": None,
        "contactEmail": None,
        "invoiceEmail": None,
        "timezone": None
    }

    def create_warehouse(self, warehouse_body):
        self.wait_until_page_loaded()
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), warehouse_body.pop("state"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), warehouse_body.pop("timezone"))
        for field in warehouse_body.keys():
            self.input_by_name(field, warehouse_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows+1)

    def check_last_warehouse(self, warehouse_body):
        self.open_last_page()
        table_cells = {
            "Warehouse name": warehouse_body["name"],
            "Warehouse number": warehouse_body["number"],
            "Timezone": warehouse_body["timezone"],
            "Warehouse address": [warehouse_body["address.zipCode"], warehouse_body["address.line1"], warehouse_body["address.line2"], warehouse_body["address.city"]],
            "Contact email": warehouse_body["contactEmail"],
            "Invoice email": warehouse_body["invoiceEmail"]
        }
        for cell, value in table_cells.items():
            self.check_last_table_item_by_header(cell, value)

    def update_last_warehouse(self, warehouse_body):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), warehouse_body.pop("state"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), warehouse_body.pop("timezone"))
        for field in warehouse_body.keys():
            self.input_by_name(field, warehouse_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_last_warehouse(self):
        warehouse = self.get_last_table_item_text_by_header("Warehouse name")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(warehouse)
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()
