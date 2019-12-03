from src.pages.distributor.distributor_portal_page import DistributorPortalPage
import re

class DistributorUsersPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def create_distributor_user(self, email, first_name, last_name, role, warehouses):
        self.click_id(self.locators.id_add_button)
        self.input_by_name("email", email)
        self.input_by_name("firstName", first_name)
        self.input_by_name("lastName", last_name)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), role)
        for checkbox in warehouses:
            self.select_checkbox_in_dialog_by_name(checkbox)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_last_distributor_user(self, email, first_name, last_name, role, warehouses):
        self.check_last_table_item_by_header("Email", email)
        self.check_last_table_item_by_header("First name", first_name)
        self.check_last_table_item_by_header("Last name", last_name)
        self.check_last_table_item_by_header("Role", role)
        splitted_warehouses = []
        for element in warehouses:
            splitted_warehouses.append((re.split(r' \(', element))[0])
        self.check_last_table_item_by_header("Warehouses", splitted_warehouses)

    def update_last_distributor_user(self, first_name, last_name, role, warehouses):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_user, self.get_table_rows_number()))
        self.input_by_name("firstName", first_name)
        self.input_by_name("lastName", last_name)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), role)
        self.clear_all_checkboxes_in_dialog()
        for checkbox in warehouses:
            self.select_checkbox_in_dialog_by_name(checkbox)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_distributor_user(self):
        full_name = self.get_last_table_item_text_by_header("First name")
        full_name += " " + self.get_last_table_item_text_by_header("Last name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_user, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()

    def create_distributor_super_user(self, email, first_name, last_name):
        self.click_id(self.locators.id_add_button)
        self.input_by_name("email", email)
        self.input_by_name("firstName", first_name)
        self.input_by_name("lastName", last_name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_last_distributor_super_user(self, email, first_name, last_name):
        self.check_last_table_item_by_header("Email", email)
        self.check_last_table_item_by_header("First name", first_name)
        self.check_last_table_item_by_header("Last name", last_name)

    def update_last_distributor_super_user(self, first_name, last_name):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_super_user, self.get_table_rows_number()))
        self.input_by_name("firstName", first_name)
        self.input_by_name("lastName", last_name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_distributor_super_user(self):
        full_name = self.get_last_table_item_text_by_header("First name")
        full_name += " " + self.get_last_table_item_text_by_header("Last name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_super_user, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()