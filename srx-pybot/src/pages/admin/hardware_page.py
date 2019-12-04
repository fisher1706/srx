from src.pages.admin.admin_portal_page import AdminPortalPage
import time

class HardwarePage(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def create_iothub(self, distributor):
        self.click_xpath(self.locators.class_button_info)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 1), "IoT Hub")
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 2), distributor)
        self.click_xpath(self.locators.class_button_ok)
        self.should_be_present_xpath("//h4[text()='IoT HUB provision information']")
        serial_number = self.get_element_text(self.locators.class_modal_dialog+self.locators.class_jumbotron+"/h3")
        self.click_xpath(self.locators.class_button_close)
        self.dialog_should_not_be_visible()
        return serial_number

    def check_last_hardware(self, serial_number=None, device_type=None, iothub=None, device_name=None, distributor=None, customer_shipto=None, distributor_user=None, customer_user=None, expiration_date=None):
        self.open_last_page_bootstrap()
        self.check_last_table_item_by_header_bootstrap("Serial Number", serial_number)
        self.check_last_table_item_by_header_bootstrap("Device Type", device_type)
        self.check_last_table_item_by_header_bootstrap("IoT Hub", iothub)
        self.check_last_table_item_by_header_bootstrap("Device name", device_name)
        self.check_last_table_item_by_header_bootstrap("Distributor", distributor)
        self.check_last_table_item_by_header_bootstrap("Customer-ShipTo", customer_shipto)
        self.check_last_table_item_by_header_bootstrap("Distributor User", distributor_user)
        self.check_last_table_item_by_header_bootstrap("Customer User", customer_user)
        self.check_last_table_item_by_header_bootstrap("Expiration Date", expiration_date)

    def update_last_iothub(self, distributor):
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

    def is_iothub_available_in_dialog(self, type_name, hub_text):
        result = False
        self.click_xpath(self.locators.class_button_info)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 1), type_name)
        self.click_xpath(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 2))
        dropdown_list_item_xpath = "//div[text()='-- select a IoTHub --']/../div"
        number_of_dropdown_list_items = self.get_element_count(dropdown_list_item_xpath)
        for index in range(1, number_of_dropdown_list_items+1):
            dropdown_list_item_text = self.get_element_text(self.locators.xpath_by_count(dropdown_list_item_xpath, index))
            if (dropdown_list_item_text == hub_text):
                result = True
                break
        else:
            result = False
        self.click_xpath(self.locators.class_button_close)
        return result

    def iothub_should_be_available(self, type_name, hub_text):
        if (self.is_iothub_available_in_dialog(type_name, hub_text)):
            self.logger.info("IoT Hub '"+hub_text+"' is found")
        else:
            self.logger.error("IoT Hub '"+hub_text+"' is not found")

    def iothub_should_not_be_available(self, type_name, hub_text):
        if (not self.is_iothub_available_in_dialog(type_name, hub_text)):
            self.logger.info("There is no IoT Hub '"+hub_text+"'")
        else:
            self.logger.error("There is IoT Hub '"+hub_text+"', but it should NOT be here")

    def create_locker(self, distributor, iothub_name):
        self.click_xpath(self.locators.class_button_info)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 1), "Locker")
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 2), iothub_name)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 3), "Standard")
        self.click_xpath(self.locators.class_button_ok)
        self.dialog_should_not_be_visible()

    def create_vending(self, distributor, iothub_name):
        self.click_xpath(self.locators.class_button_info)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 1), "Vending")
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.bootstrap_select_box, 2), iothub_name)
        self.click_xpath(self.locators.class_button_ok)
        self.dialog_should_not_be_visible()