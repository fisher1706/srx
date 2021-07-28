from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class DistributorSmartShelvesPage(DistributorPortalPage):
    smart_shelves_body = {
        "assign_to": None,
        "door_number": None
    }
    xpath_merge_cells = "//span[text()='MERGE CELLS']"
    xpath_split_cells = "//span[text()='SPLIT CELL']"

    def open_smart_shelves(self):
        self.sidebar_hardware()
        self.click_tab_by_name("Smart shelves")
        self.wait_until_page_loaded()

    def update_smart_shelves(self, smart_shelves_body):
        self.open_last_page()
        self.wait_until_page_loaded()
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        self.should_be_disabled_xpath("//input[@name='serialNumber']")
        self.should_be_disabled_xpath("//input[@name='cellsQuantity']")
        self.should_be_disabled_xpath(f"{Locator.xpath_dropdown_in_dialog(2)}//input")
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), smart_shelves_body["assign_to"])
        self.should_be_enabled_xpath(Locator.xpath_dropdown_in_dialog(2))
        # input Door Number
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), smart_shelves_body["door_number"])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_last_smart_shelf(self, smart_shelves_body):
        table_cells = {
            "Serial Number": smart_shelves_body["serialNumber"],
            "Assigned Device Name": smart_shelves_body["assign_to"],
            "Qnty of Cells": "4"
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def merge_cells(self, number_of_cells, is_planogram=False, door_number=None):
        if (not is_planogram):
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
            for x in range(number_of_cells):
                self.click_xpath(f"//div[@data-cell='{x}']")
            self.click_xpath(self.xpath_merge_cells)
            self.click_xpath(Locator.xpath_submit_button)
            self.click_xpath(Locator.xpath_label_confirm)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()
        else:
            for x in range(1, number_of_cells + 1):
                self.click_xpath(f"//div[@data-door={door_number}]//div[@data-cell='{x}']")
            self.click_xpath(self.xpath_merge_cells)
            self.click_xpath(f"//div[@data-door={door_number}]//div[@data-cell='1']")

    def split_cells(self, position_of_cell, is_planogram=False, door_number=None):
        if (not is_planogram):
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
            self.click_xpath(f"//div[@data-cell='{position_of_cell}']")
            self.click_xpath(self.xpath_split_cells)
            self.click_xpath(Locator.xpath_submit_button)
            self.click_xpath(Locator.xpath_label_confirm)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()
        else:
            self.click_xpath(f"//div[@data-cell='{position_of_cell}']")
            self.click_xpath(self.xpath_split_cells)
            self.click_xpath(f"//div[@data-door={door_number}]//div[@data-cell='1']")

    def check_cells_number(self, number_of_cells, is_planogram=False, door_number=None):
        if (not is_planogram):
            self.check_last_table_item_by_header("Qnty of Cells", "4")
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
            self.elements_count_should_be("//div[@data-cell]", number_of_cells)
            self.click_xpath(Locator.xpath_label_cancel)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()
        else:
            self.elements_count_should_be(f"//div[@data-door={door_number}]//div[@data-cell]", number_of_cells)

    def assign_smart_shelf_to_locker(self, smart_shelf, locker, door_number):
        self.open_last_page()
        row_number = self.get_row_of_table_item_by_header(smart_shelf, "Serial Number")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, row_number)+Locator.xpath_edit_button)
        self.wait_until_progress_bar_loaded()
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), locker)
        self.should_be_enabled_xpath(Locator.xpath_dropdown_in_dialog(2))
        # input Door Number
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), door_number)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
