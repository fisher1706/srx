from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.tools import Tools
from src.resources.locator import Locator
import random
import time

class HardwarePage(AdminPortalPage):
    xpath_weight_radio = "//input[@name='noWeight' and @type='radio' and @value='false']"
    xpath_no_weight_radio = "//input[@name='noWeight' and @type='radio' and @value='true']"
    xpath_door_serial_number_title = "//div[text()='Door Serial Number']"
    xpath_door_serial_number = f"{xpath_door_serial_number_title}/../div[2]"
    xpath_smart_shelf_title = "//div[text()='Smart Shelf Serial Number']"
    xpath_smart_shelf_absence_title = "//span[text()='There is no smart shelf assigned']"

    def create_iothub(self, distributor):
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), "IoT Hub")
        self.get_element_by_xpath(Locator.xpath_dropdown_in_dialog(6))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(6), distributor)
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_page_loaded()
        self.get_element_by_xpath("//h6[text()='IoTHub provision information']")
        self.get_element_by_xpath("//div[text()='Access Key:']/../span")
        serial_number = self.get_element_text("//div[text()='Access Key:']/../span")
        self.click_xpath(Locator.xpath_close_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        return serial_number

    def check_last_hardware(self, serial_number=None, device_type=None, iothub=None, device_name=None, distributor=None, customer_shipto=None, distributor_user=None, customer_user=None, expiration_date=None, device_subtype=None):
        self.get_element_by_xpath(Locator.xpath_table_row)
        self.open_last_page()
        self.get_element_by_xpath(Locator.xpath_table_row)
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
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, self.get_table_rows_number())+Locator.xpath_edit_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(7), distributor)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def remove_last_hardware(self, hardware_type, serial_number=None):
        if (hardware_type == "IOTHUB"):
            type_title = Locator.xpath_remove_button
        elif (hardware_type == "LOCKER"):
            type_title = Locator.xpath_remove_button
        elif (hardware_type == "VENDING"):
            type_title = Locator.xpath_remove_button
        self.open_last_page()
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, self.get_table_rows_number())+type_title)
        if (serial_number is not None):
            self.delete_dialog_should_be_about(serial_number)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def is_iothub_available_in_dialog(self, type_name, hub_text):
        result = False
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), type_name)
        self.click_xpath(Locator.xpath_dropdown_in_dialog(5))
        number_of_dropdown_list_items = self.get_element_count(Locator.xpath_dropdown_list_item+"/div")
        for index in range(1, number_of_dropdown_list_items+1):
            dropdown_list_item_text = self.get_element_text(Locator.xpath_by_count(Locator.xpath_dropdown_list_item+"/div", index))
            if (dropdown_list_item_text == hub_text):
                result = True
                break
        else:
            result = False
        self.click_xpath(Locator.xpath_close_button)
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
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), "Locker")
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(5), iothub_name)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(7), "Standard")
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def create_vending(self, distributor, iothub_name):
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), "Vending")
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(5), iothub_name)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def configure_locker_door(self, door_number=None, serial_number=None, is_weight=False):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, self.get_table_rows_number())+Locator.xpath_planogram_button)
        self.get_element_by_xpath(Locator.xpath_configure_button)
        if (door_number is None):
            count = self.get_element_count(Locator.xpath_configure_button)
            door_number = random.choice(range(0, count))+1
        if (serial_number is None):
            serial_number = Tools.random_string_u()
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_configure_button, door_number))
        if (is_weight == False):
            xpath_radio = self.xpath_no_weight_radio
        else:
            xpath_radio = self.xpath_weight_radio
        self.click_xpath(f"{xpath_radio}/../..")
        self.input_by_name("doorSerial", serial_number)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        data = {
            "doors_count": count,
            "door": door_number,
            "weight": is_weight,
            "serial_number": serial_number
        }
        return data

    def check_locker_door(self, doors_data):
        assert doors_data["serial_number"] == self.get_element_text(self.xpath_door_serial_number), "The Door SN is incorrect"
        if (doors_data["weight"] == False):
            smart_shelves = self.get_element_count(self.xpath_smart_shelf_absence_title)
            assert doors_data["doors_count"] == smart_shelves + 1, "The number of noWeight doors is incorrect"