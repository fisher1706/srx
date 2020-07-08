from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
import re

class DistributorUsersPage(DistributorPortalPage):
    distributor_user_body = {
        "firstName": None,
        "lastName": None,
        "email": None,
        "role": None,
        "warehouses": None
    }

    distributor_superuser_body = {
        "firstName": None,
        "lastName": None,
        "email": None
    }

    def create_distributor_user(self, distributor_user_body):
        self.wait_until_page_loaded()
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), distributor_user_body.pop("role"))
        for checkbox in distributor_user_body.pop("warehouses"):
            self.select_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_user_body.keys():
            self.input_by_name(field, distributor_user_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows+1)

    def check_last_distributor_user(self, distributor_user_body):
        self.open_last_page()
        splitted_warehouses = []
        for element in distributor_user_body.pop("warehouses"):
            splitted_warehouses.append((re.split(r' \(', element))[0])
        table_cells = {
            "Email": distributor_user_body["email"],
            "First name": distributor_user_body["firstName"],
            "Last name": distributor_user_body["lastName"],
            "Role": distributor_user_body["role"],
            "Warehouses": splitted_warehouses
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def update_last_distributor_user(self, distributor_user_body):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), distributor_user_body.pop("role"))
        for checkbox in distributor_user_body.pop("warehouses"):
            self.select_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_user_body.keys():
            self.input_by_name(field, distributor_user_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_distributor_user(self):
        full_name = self.get_last_table_item_text_by_header("First name")
        full_name += " " + self.get_last_table_item_text_by_header("Last name")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()

    def create_distributor_super_user(self, distributor_superuser_body):
        self.wait_until_page_loaded()
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_add_button)
        for field in distributor_superuser_body.keys():
            self.input_by_name(field, distributor_superuser_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows+1)

    def check_last_distributor_super_user(self, distributor_superuser_body):
        self.open_last_page()
        table_cells = {
            "Email": distributor_superuser_body["email"],
            "First name": distributor_superuser_body["firstName"],
            "Last name": distributor_superuser_body["lastName"]
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def update_last_distributor_super_user(self, distributor_superuser_body):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        for field in distributor_superuser_body.keys():
            self.input_by_name(field, distributor_superuser_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_distributor_super_user(self):
        full_name = self.get_last_table_item_text_by_header("First name")
        full_name += " " + self.get_last_table_item_text_by_header("Last name")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()