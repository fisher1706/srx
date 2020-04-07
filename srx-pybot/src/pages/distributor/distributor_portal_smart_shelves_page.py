from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class DistributorSmartShelvesPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.smart_shelves_body = {
            "assign_to": None,
            "door_number": None
        }
        self.xpath_merge_cells = "//span[text()='MERGE CELLS']"
        self.xpath_split_cells = "//span[text()='SPLIT CELL']"

    def open_smart_shelves(self):
        self.sidebar_hardware()
        self.click_tab_by_name("Smart shelves")
        self.wait_until_page_loaded(7)

    def update_smart_shelves(self, smart_shelves_body):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves_dist, self.get_table_rows_number()))
        self.should_be_disabled_xpath("//input[@name='serialNumber']")
        self.should_be_disabled_xpath("//input[@name='cellsQuantity']")
        self.should_be_disabled_xpath(f"{self.locators.xpath_dropdown_in_dialog(2)}//input")
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), smart_shelves_body["assign_to"])
        self.should_be_enabled_xpath(self.locators.xpath_dropdown_in_dialog(2))
        # input Door Number
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), smart_shelves_body["door_number"])
        self.click_xpath(self.locators.xpath_submit_button)
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
        if (is_planogram == False):
            self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves_dist, self.get_table_rows_number()))
            for x in range(number_of_cells):
                self.click_xpath(f"//div[@data-cell='{x}']")
            self.click_xpath(self.xpath_merge_cells)
            self.click_xpath(self.locators.xpath_submit_button)
            self.click_xpath(self.locators.xpath_label_confirm)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()
        if (is_planogram == True):
            for x in range(1, number_of_cells + 1):
                self.click_xpath(f"//div[@data-door={door_number}]//div[@data-cell='{x}']")
            self.click_xpath(self.xpath_merge_cells)
            self.wait_until_progress_bar_loaded()
            self.click_xpath(f"//div[@data-door={door_number}]//div[@data-cell='1']")

    def split_cells(self, position_of_cell, is_planogram=False, door_number=None):
        if (is_planogram == False):
            self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves_dist, self.get_table_rows_number()))
            self.click_xpath(f"//div[@data-cell='{position_of_cell}']")
            self.click_xpath(self.xpath_split_cells)
            self.click_xpath(self.locators.xpath_submit_button)
            self.click_xpath(self.locators.xpath_label_confirm)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()
        if (is_planogram == True):
            self.click_xpath(f"//div[@data-cell='{position_of_cell}']")
            self.click_xpath(self.xpath_split_cells)
            self.wait_until_progress_bar_loaded()
            self.click_xpath(f"//div[@data-door={door_number}]//div[@data-cell='1']")

    def check_cells_number(self, number_of_cells, is_planogram=False, door_number=None):
        if (is_planogram == False):
            self.check_last_table_item_by_header("Qnty of Cells", "4")
            self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_smart_shelves_dist, self.get_table_rows_number()))
            self.elements_count_should_be("//div[@data-cell]", number_of_cells)
            self.click_xpath(self.locators.xpath_label_cancel)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()
        if (is_planogram == True):
            self.elements_count_should_be(f"//div[@data-door={door_number}]//div[@data-cell]", number_of_cells)

    def assign_smart_shelf_to_locker(self, smart_shelf, locker, door_number):
        row_number = self.get_row_of_table_item_by_header(smart_shelf, "Serial Number")
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, row_number)+self.locators.title_edit_smart_shelves_dist)
        self.wait_until_progress_bar_loaded()
        # input Assign To and check if Door Number is editable
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), locker)
        self.should_be_enabled_xpath(self.locators.xpath_dropdown_in_dialog(2))
        # input Door Number
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), door_number)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
