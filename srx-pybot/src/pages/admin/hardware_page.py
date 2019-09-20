from src.pages.admin.admin_portal_page import AdminPortalPage

class HardwarePage(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def create_iot_hub(self, distributor):
        self.click_xpath(self.locators.class_button_info)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 1), "IoT Hub")
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 2), distributor)
        self.click_xpath(self.locators.class_button_ok)
        self.should_be_present_xpath("//h4[text()='IoT HUB provision information']")
        serial_number = self.get_element_text(self.locators.class_modal_dialog+self.locators.class_jumbotron)
        self.click_xpath(self.locators.class_button_close)
        self.dialog_should_not_be_visible()
        return serial_number

    def check_last_hardware(self, serial_number, device_type, iot_hub=None, device_name=None, distributor=None, customer_shipto=None, distributor_user=None, customer_user=None, expiration_date=None):
        self.open_last_page_bootstrap()
        self.check_last_table_item_by_header_bootstrap("Serial Number", serial_number)
        self.check_last_table_item_by_header_bootstrap("Device Type", device_type)
        self.check_last_table_item_by_header_bootstrap("IoT Hub", iot_hub)
        self.check_last_table_item_by_header_bootstrap("Device name", device_name)
        self.check_last_table_item_by_header_bootstrap("Distributor", distributor)
        self.check_last_table_item_by_header_bootstrap("Customer-ShipTo", customer_shipto)
        self.check_last_table_item_by_header_bootstrap("Distributor User", distributor_user)
        self.check_last_table_item_by_header_bootstrap("Customer User", customer_user)
        self.check_last_table_item_by_header_bootstrap("Expiration Date", expiration_date)

    def update_last_iot_hub(self, distributor):
        self.open_last_page_bootstrap()
        self.click_xpath(self.locators.xpath_by_count(self.locators.class_button_success, self.get_table_rows_number_bootstrap()))
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 1), distributor)
        self.click_xpath(self.locators.class_button_ok)
        self.dialog_should_not_be_visible()

    def remove_last_hardware(self):
        self.open_last_page_bootstrap()
        self.click_xpath(self.locators.xpath_by_count(self.locators.class_button_danger, self.get_table_rows_number_bootstrap()))
        self.click_xpath("//span[text()='Yes, delete item']/..")
        self.dialog_should_not_be_visible()

