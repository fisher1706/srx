from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.tools import Tools
import random

class HardwarePage(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.xpath_weight_radio = "//input[@name='noWeight' and @type='radio' and @value='false']"
        self.xpath_no_weight_radio = "//input[@name='noWeight' and @type='radio' and @value='true']"
        self.xpath_door_serial_number_title = "//div[text()='Door Serial Number']"
        self.xpath_door_serial_number = f"{self.xpath_door_serial_number_title}/../div[2]"
        self.xpath_smart_shelf_title = "//div[text()='Smart Shelf Serial Number']"

    def create_iothub(self, distributor):
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), "IoT Hub")
        self.should_be_present_xpath(self.locators.xpath_dropdown_in_dialog(3))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(3), distributor)
        self.click_xpath(self.locators.xpath_submit_button)
        self.wait_until_page_loaded()
        self.should_be_present_xpath("//h6[text()='IoTHub provision information']")
        self.should_be_present_xpath("//div[text()='Access Key:']/../span")
        serial_number = self.get_element_text("//div[text()='Access Key:']/../span")
        self.click_xpath(self.locators.xpath_close_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        return serial_number

    def check_last_hardware(self, serial_number=None, device_type=None, iothub=None, device_name=None, distributor=None, customer_shipto=None, distributor_user=None, customer_user=None, expiration_date=None, device_subtype=None):
        self.open_last_page()
        self.check_last_table_item_by_header("Serial Number", serial_number)
        self.check_last_table_item_by_header("Device Type", device_type)
        self.check_last_table_item_by_header("IoT Hub", iothub)
        self.check_last_table_item_by_header("Device name", device_name)
        self.check_last_table_item_by_header("Distributor", distributor)
        self.check_last_table_item_by_header("Customer-ShipTo", customer_shipto)
        self.check_last_table_item_by_header("Distributor User", distributor_user)
        self.check_last_table_item_by_header("Customer User", customer_user)
        self.check_last_table_item_by_header("Expiration Date", expiration_date)
        self.check_last_table_item_by_header("Device Sub-Type", device_subtype)

    def update_last_iothub(self, distributor):
        self.open_last_page()
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, self.get_table_rows_number())+self.locators.title_edit_iothub)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(4), distributor)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def remove_last_hardware(self, hardware_type, serial_number=None):
        if (hardware_type == "IOTHUB"):
            type_title = self.locators.title_delete_iothub
        elif (hardware_type == "LOCKER"):
            type_title = self.locators.title_delete_locker
        elif (hardware_type == "VENDING"):
            type_title = self.locators.title_delete_vending
        self.open_last_page()
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, self.get_table_rows_number())+type_title)
        if (serial_number is not None):
            self.delete_dialog_should_be_about(serial_number)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def is_iothub_available_in_dialog(self, type_name, hub_text):
        result = False
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), type_name)
        self.click_xpath(self.locators.xpath_dropdown_in_dialog(2))
        number_of_dropdown_list_items = self.get_element_count(self.locators.xpath_dropdown_list_item+"/div")
        for index in range(1, number_of_dropdown_list_items+1):
            dropdown_list_item_text = self.get_element_text(self.locators.xpath_by_count(self.locators.xpath_dropdown_list_item+"/div", index))
            if (dropdown_list_item_text == hub_text):
                result = True
                break
        else:
            result = False
        self.click_xpath(self.locators.xpath_close_button)
        return result

    def iothub_should_be_available(self, type_name, hub_text):
        if (self.is_iothub_available_in_dialog(type_name, hub_text)):
            self.logger.info(f"IoT Hub '{hub_text}' is found")
        else:
            self.logger.error(f"IoT Hub '{hub_text}' is not found")

    def iothub_should_not_be_available(self, type_name, hub_text):
        if (not self.is_iothub_available_in_dialog(type_name, hub_text)):
            self.logger.info(f"There is no IoT Hub '{hub_text}'")
        else:
            self.logger.error(f"There is IoT Hub '{hub_text}', but it should NOT be here")

    def create_locker(self, distributor, iothub_name):
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), "Locker")
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), iothub_name)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(4), "Standard")
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def create_vending(self, distributor, iothub_name):
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), "Vending")
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), iothub_name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def configure_locker_door(self, door_number=None, serial_number=None, is_weight=False):
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, self.get_table_rows_number())+self.locators.title_configure)
        if (door_number is None):
            count = self.get_element_count(self.locators.title_edit_door)
            door_number = random.choice(range(0, count))+1
        if (serial_number is None):
            serial_number = Tools.random_string_u()
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_door, door_number))
        if (is_weight == False):
            xpath_radio = self.xpath_no_weight_radio
        else:
            xpath_radio = self.xpath_weight_radio
        self.click_xpath(f"{xpath_radio}/../..")
        self.input_by_name("doorSerial", serial_number)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        data = {
            "doors_count": count,
            "door": door_number,
            "weight": is_weight,
            "serial_number": serial_number
        }
        return data

    def check_locker_door(self, doors_data):
        assert doors_data["serial_number"] == self.get_element_text(self.locators.xpath_by_count(self.xpath_door_serial_number, doors_data["door"])), "The Door SN is incorrect"
        if (doors_data["weight"] == False):
            smart_shelves = self.get_element_count(self.xpath_smart_shelf_title)
            assert doors_data["doors_count"] == smart_shelves + 1, "The number of noWeight doors is incorrect"
            for door in range(1, doors_data["doors_count"]+1):
                if (door != doors_data["door"]):
                    self.should_be_present_xpath(f"{self.xpath_door_serial_number_title}/../../..{self.xpath_smart_shelf_title}")
