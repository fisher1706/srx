from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.tools import Tools
from src.resources.locator import Locator

class RfidPage(DistributorPortalPage):
    xpath_rfid_add = f"{Locator.xpath_dialog+Locator.xpath_button_type}//span[text()='Add']"

    def add_rfid_label(self, label=None):
        if label is None:
            label = Tools.random_string_u()
        self.click_id(Locator.id_add_button)
        self.wait_until_page_loaded()
        self.input_by_name("labelId", label)
        self.click_xpath(self.xpath_rfid_add)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded(5)
        return label

    def check_last_rfid_label(self, label, status):
        self.check_last_table_item_by_header("RFID", label)
        self.check_last_table_item_by_header("State", status)

    def update_last_rfid_label_status(self, status):
        self.get_element_by_xpath(Locator.xpath_table_row)
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_status_button, self.get_table_rows_number()))
        self.click_xpath(f"{Locator.xpath_dialog}{Locator.xpath_button}//span[text()='{status}']")
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def unassign_last_rfid_label(self):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_unassign_button, self.get_table_rows_number()))
        self.click_xpath(Locator.xpath_button_by_name("Yes, unassign EPC"))
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def import_rfid_as_available(self, rfids):
        Tools.generate_csv("rfids_as_available.csv", rfids)
        self.import_csv(Locator.id_upload_rfid_available, "rfids_as_available.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()

    def import_rfid(self, rfids):
        Tools.generate_csv("rfids.csv", rfids)
        self.import_csv(Locator.id_upload_rfid_csv, "rfids.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()
