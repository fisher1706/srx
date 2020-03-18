from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.tools import Tools

class RfidPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.xpath_rfid_add = f"{self.locators.xpath_submit_button}//span[text()='Add']"

    def select_shipto_sku(self, shipto, sku):
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), shipto)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), sku)
        self.wait_until_page_loaded()

    def add_rfid_label(self, label=None):
        if (label is None):
            label = Tools.random_string_u()
        self.click_id(self.locators.id_add_button)
        self.input_by_name("labelId", label)
        self.click_xpath(self.xpath_rfid_add)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded(5)
        return label

    def check_last_rfid_label(self, label, status):
        self.check_last_table_item_by_header("RFID", label)
        self.check_last_table_item_by_header("State", status)

    def update_last_rfid_label_status(self, status):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_status, self.get_table_rows_number()))
        self.click_xpath(f"{self.locators.xpath_dialog}{self.locators.xpath_button}//span[text()='{status}']")
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def unassign_last_rfid_label(self):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_unassign, self.get_table_rows_number()))
        self.click_xpath(self.locators.xpath_button_by_name("Yes, unassign EPC"))
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()