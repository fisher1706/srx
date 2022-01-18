import re
from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.api.distributor.user_api import UserApi

class DistributorUsersPage(DistributorPortalPage):
    distributor_user_body = {
        "firstName": None,
        "lastName": None,
        "email": None,
        "role": None,
        "warehouses": None,
        "position": None
    }

    distributor_superuser_body = {
        "firstName": None,
        "lastName": None,
        "email": None,
        "position": None
    }

    def create_distributor_user(self, distributor_user_body):
        ua = UserApi(self.context)
        start_number_of_rows = ua.get_distributor_user(full=True)["totalElements"]
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), distributor_user_body.pop("role"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), distributor_user_body.pop("position"))
        for checkbox in distributor_user_body.pop("warehouses"):
            self.select_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_user_body.keys():
            self.input_by_name(field, distributor_user_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.last_page(10)
        self.get_element_by_xpath(Locator.xpath_get_row_by_index(start_number_of_rows%10))

    def check_last_distributor_user(self, distributor_user_body):
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
        for cell, value in table_cells.items():
            self.check_table_item(value, header=cell, last=True)

    def update_last_distributor_user(self, distributor_user_body):
        self.click_xpath(Locator.xpath_last_role_row+Locator.xpath_edit_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), distributor_user_body.pop("role"))
        for checkbox in distributor_user_body.pop("warehouses"):
            self.select_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_user_body.keys():
            self.input_by_name(field, distributor_user_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_distributor_user(self, value):
        self.click_xpath(Locator.xpath_last_role_row+Locator.xpath_remove_button)
        self.delete_dialog_should_be_about(value)
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()

    def create_distributor_super_user(self, distributor_superuser_body):
        self.wait_until_page_loaded()
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), distributor_superuser_body.pop("role"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), distributor_superuser_body.pop("position"))
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
        for cell, value in table_cells.items():
            self.check_last_table_item_by_header(cell, value)

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
