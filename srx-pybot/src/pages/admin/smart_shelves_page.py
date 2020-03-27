from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.tools import Tools
import random

class SmartShelves(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.smart_shelves_body = {
            "serialNumber": None,
            "distributor": None,
            "assign_to": None,
            "door_number": None
        }
        self.xpath_merge_cells = "//span[text()='MERGE CELLS']"
        self.xpath_split_cells = "//span[text()='SPLIT CELL']"

    def open_smart_shelves(self):
        self.sidebar_hardware()
        self.click_tab_by_name("Smart Shelves")

    def create_smart_shelves(self, smart_shelves_body):
        self.click_id(self.locators.id_add_button)
        # input Serial Number
        self.input_by_name("serialNumber", smart_shelves_body["serialNumber"])
        # input Distributor and check if Assign To is editable
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), smart_shelves_body["distributor"])
        self.should_be_enabled_xpath(self.locators.xpath_dropdown_in_dialog(2))
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), smart_shelves_body["assign_to"])
        self.should_be_enabled_xpath(self.locators.xpath_dropdown_in_dialog(3))
        # input Door Number
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(3), smart_shelves_body["door_number"])
        self.click_xpath(self.locators.xpath_submit_button)
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
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves, self.get_table_rows_number()))
        # input Serial Number
        self.input_by_name("serialNumber", smart_shelves_body["serialNumber"])
        # change Distributor and check if fields "Assign To" and "Door Number" become empty
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), smart_shelves_body["distributor"])
        self.should_be_disabled_xpath(f"{self.locators.xpath_dropdown_in_dialog(3)}//input", wait=True)
        self.element_text_should_be_empty(self.locators.xpath_dropdown_in_dialog(2))
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), smart_shelves_body["assign_to"])
        self.should_be_enabled_xpath(self.locators.xpath_dropdown_in_dialog(3))
        # input Door Number
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(3), smart_shelves_body["door_number"])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_smart_shelf(self, serial_number):
        shelf_serial_number = self.get_last_table_item_text_by_header("Serial Number")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_smart_shelves, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(f"{serial_number}")
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()

    def merge_cells(self, number_of_cells):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves, self.get_table_rows_number()))
        for x in range(number_of_cells):
            self.click_xpath(f"//div[@data-cell='{x}']")
        self.click_xpath(self.xpath_merge_cells)
        self.click_xpath(self.locators.xpath_submit_button)
        self.click_xpath(self.locators.xpath_label_confirm)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def split_cells(self, position_of_cell):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves, self.get_table_rows_number()))
        self.click_xpath(f"//div[@data-cell='{position_of_cell}']")
        self.click_xpath(self.xpath_split_cells)
        self.click_xpath(self.locators.xpath_submit_button)
        self.click_xpath(self.locators.xpath_label_confirm)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_cells_number(self, number_of_cells):
        self.check_last_table_item_by_header("Qnty of Cells", "4")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves, self.get_table_rows_number()))
        self.elements_count_should_be("//div[@data-cell]", number_of_cells)
        self.click_xpath(self.locators.xpath_label_cancel)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
