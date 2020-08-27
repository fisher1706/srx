from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.tools import Tools
from src.resources.locator import Locator
import random

class SmartShelvesPage(AdminPortalPage):
    smart_shelves_body = {
        "serialNumber": None,
        "distributor": None,
        "assign_to": None,
        "door_number": None
    }
    xpath_merge_cells = "//span[text()='MERGE CELLS']"
    xpath_split_cells = "//span[text()='SPLIT CELL']"

    def open_smart_shelves(self):
        self.sidebar_hardware()
        self.click_tab_by_name("Smart Shelves")
        self.open_last_page()
        self.get_element_by_xpath(Locator.xpath_table_row)

    def create_smart_shelves(self, smart_shelves_body):
        self.click_id(Locator.id_add_button)
        # input Serial Number
        self.input_by_name("serialNumber", smart_shelves_body["serialNumber"])
        # input Distributor and check if Assign To is editable
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), smart_shelves_body["distributor"])
        self.should_be_enabled_xpath(Locator.xpath_dropdown_in_dialog(2))
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), smart_shelves_body["assign_to"])
        self.should_be_enabled_xpath(Locator.xpath_dropdown_in_dialog(3))
        # input Door Number
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(3), smart_shelves_body["door_number"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
    
    def check_last_smart_shelf(self, smart_shelves_body):
        table_cells = {
            "Serial Number": smart_shelves_body["serialNumber"],
            "Assigned Device": smart_shelves_body["assign_to"],
            "Distributor": smart_shelves_body["distributor"],
            "Qnty of Cells": "4"
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])
    
    def update_smart_shelves(self, smart_shelves_body):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        # input Serial Number
        self.input_by_name("serialNumber", smart_shelves_body["serialNumber"])
        # change Distributor and check if fields "Assign To" and "Door Number" become empty
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), smart_shelves_body["distributor"])
        self.should_be_disabled_xpath(f"{Locator.xpath_dropdown_in_dialog(3)}//input", wait=True)
        self.element_text_should_be_empty(Locator.xpath_dropdown_in_dialog(2))
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), smart_shelves_body["assign_to"])
        self.should_be_enabled_xpath(Locator.xpath_dropdown_in_dialog(3))
        # input Door Number
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(3), smart_shelves_body["door_number"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_smart_shelf(self, serial_number):
        shelf_serial_number = self.get_last_table_item_text_by_header("Serial Number")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(f"{serial_number}")
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()

    def merge_cells(self, number_of_cells):
        self.get_element_by_xpath(Locator.xpath_edit_button)
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        for x in range(number_of_cells):
            self.click_xpath(f"//div[@data-cell='{x}']")
        self.click_xpath(self.xpath_merge_cells)
        self.click_xpath(Locator.xpath_submit_button)
        self.click_xpath(Locator.xpath_label_confirm)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def split_cells(self, position_of_cell):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        self.click_xpath(f"//div[@data-cell='{position_of_cell}']")
        self.click_xpath(self.xpath_split_cells)
        self.click_xpath(Locator.xpath_submit_button)
        self.click_xpath(Locator.xpath_label_confirm)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_cells_number(self, number_of_cells):
        self.get_element_by_xpath(Locator.xpath_table_row)
        self.check_last_table_item_by_header("Qnty of Cells", "4")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        self.elements_count_should_be("//div[@data-cell]", number_of_cells)
        self.click_xpath(Locator.xpath_label_cancel)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_first_door_is_unavaliable(self, locker, create=None): 
        if (create is None):
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        elif (create):
            self.click_id(Locator.id_add_button)
            # input Serial Number
            self.input_by_name("serialNumber", Tools.random_string_u())
            # input Distributor
            self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), self.data.distributor_name)
        # input Assign To
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), locker)
        # check Door Number
        self.click_xpath(Locator.xpath_dropdown_in_dialog(3))
        text = self.get_element_text(f"{Locator.xpath_dropdown_list_item}/div")
        if (f"{text}" == "2"):
            self.logger.info("First door is unavailable as expected")
        else:
            self.logger.error("First door shoud not be avaliable")
        self.click_xpath(Locator.xpath_dropdown_in_dialog(3))
        self.click_xpath(Locator.xpath_label_cancel)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
    
    def clear_fields_smart_shelves(self, distributor=None, locker=None):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        self.element_should_have_text(Locator.xpath_dropdown_in_dialog(3), "1")
        if (locker is not None):
            self.click_xpath(f"{Locator.xpath_dropdown_in_dialog(2)}/div/div[2]/div")
        if (distributor is not None):
            self.click_xpath(f"{Locator.xpath_dropdown_in_dialog(1)}/div/div[2]/div")
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        
    def assign_smart_shelf_locker_planogram(self, locker, smart_shelf):
        self.get_element_by_xpath(Locator.xpath_table_row)
        self.open_last_page()
        self.get_element_by_xpath(Locator.xpath_table_row)
        locker_row = self.get_row_of_table_item_by_header(locker, "Serial Number")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, locker_row)+Locator.xpath_planogram_button)
        self.get_element_by_xpath(Locator.xpath_configure_button)
        self.click_xpath(Locator.xpath_configure_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), smart_shelf)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_smart_shelf_unavailable_via_planogram(self, locker, smart_shelf, in_list=False):
        self.wait_until_page_loaded()
        self.get_element_by_xpath(Locator.xpath_table_row)
        locker_row = self.scan_table(scan_by=locker, column_header="Serial Number")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, locker_row)+Locator.xpath_planogram_button)
        self.get_element_by_xpath(Locator.xpath_configure_button)
        self.click_xpath(Locator.xpath_configure_button)
        self.click_xpath(Locator.xpath_dropdown_in_dialog(1))
        self.input_data_xpath(smart_shelf, f"{Locator.xpath_dropdown_in_dialog(1)}//input")
        self.get_element_by_xpath(Locator.xpath_dropdown_list_item)
        text = self.get_element_text(f"{Locator.xpath_dropdown_list_item}/div")
        if (in_list):
            if (f"{text}" == f"{smart_shelf}"):
                self.logger.info(f"There is {smart_shelf} as expected")
            else:
                self.logger.error(f"Smart Shelf {smart_shelf} should be in the list")
        else:
            if (f"{text}" == f"{smart_shelf}"):
                self.logger.error(f"Smart Shelf {smart_shelf} should not be in the list")
            else:
                self.logger.info(f"There is no {smart_shelf} as expected")
        self.click_xpath(Locator.xpath_close_button)
        self.dialog_should_not_be_visible()

