from src.pages.admin.admin_portal_page import AdminPortalPage
import time

class DistributorAdminPage(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.distributor_body = {
            "name": None,
            "invoiceEmail": None,
            "address.line1": None,
            "address.line2": None,
            "address.city": None,
            "address.zipCode": None,
            "billingDelay": None
        }

    def create_distributor(self, distributor_body, state, bill_by, checkbox_list):
        self.click_id(self.locators.id_add_button)
        for checkbox in checkbox_list:
            self.select_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_body.keys():
            self.input_by_name(field, distributor_body[field])
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), state)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), bill_by)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_last_distributor(self, distributor_body, checkbox_list):
        primary_address = " ".join([distributor_body["address.line1"], distributor_body["address.line2"], distributor_body["address.city"], "MA", distributor_body["address.zipCode"]])
        table_cells = {
            "Name": distributor_body["name"],
            "Invoice Email": distributor_body["invoiceEmail"],
            "Primary Address": primary_address,
            "Billing Delay": distributor_body["billingDelay"],
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])
        table_cells_checkbox = ["Process.Fee", "SupplyForce", "User Data", "Agreements", "Billing Info"]
        row_number = self.get_table_rows_number()
        for cell_checkbox in table_cells_checkbox:
            column = self.get_header_column(cell_checkbox)
            self.should_be_present_xpath(f"{self.locators.xpath_table_item(row_number, column)}//span/div")

    def update_last_distributor(self, distributor_body, state, bill_by, checkbox_list, ship_to_level):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_distributor, self.get_table_rows_number()))
        for checkbox in checkbox_list:
            self.unselect_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_body.keys():
            self.input_by_name(field, distributor_body[field])
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), state)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), bill_by)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(3), ship_to_level)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_distributor(self):
        full_name = self.get_last_table_item_text_by_header("Name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_distributor, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()
