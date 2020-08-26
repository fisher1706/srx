from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class SerializationPage(DistributorPortalPage):
    serial_number_body = {
        "number": None,
        "lot": None,
        "dateManufacture": None,
        "dateShipment": None,
        "dateExpiration": None,
        "dateWarrantyExpires": None
    }
    xpath_save_serial_number = f"{Locator.xpath_button_type}/span[text()='Save']"

    def add_serial_number(self, serial_number_body):
        self.click_id(Locator.id_add_button)
        for field in serial_number_body.keys():
            self.input_by_name(field, serial_number_body[field])
        self.click_xpath(self.xpath_save_serial_number)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_last_serial_number(self, serial_number_body):
        table_cells = {
            "Serial Number": serial_number_body["number"],
            "Lot": serial_number_body["lot"],
            "Status": serial_number_body.get("status"),
            "DoS (Date of Shipment)": serial_number_body["dateShipment"],
            "DoM (Date of Manufacture)": serial_number_body["dateManufacture"],
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def update_last_serial_number(self, serial_number_body):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        for field in serial_number_body.keys():
            self.input_by_name(field, serial_number_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def update_last_serial_number_status(self, status):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_status_button, self.get_table_rows_number()))
        self.click_xpath(f"{Locator.xpath_dialog}{Locator.xpath_button}//span[text()='{status}']")
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_last_serial_number(self, number):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()