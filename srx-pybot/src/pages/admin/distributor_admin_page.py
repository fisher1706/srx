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
        self.table_cells_checkbox = {
            "Process.Fee": True,
            "SupplyForce": True,
            "User Data": True,
            "Agreements": True,
            "Billing Info": True
        }

    def create_distributor(self, distributor_body, state, bill_by, checkbox_list):
        check_mark = self.get_element_count(f"{self.locators.xpath_table}//span/div")
        self.click_id(self.locators.id_add_button)
        for checkbox in checkbox_list:
            self.select_checkbox_in_dialog_by_name(checkbox)
        for field in distributor_body.keys():
            self.input_by_name(field, distributor_body[field])
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), state)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), bill_by)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        return check_mark

    def check_last_distributor(self, distributor_body, state_short_code, table_cells_checkbox, check_mark):
        primary_address = " ".join([distributor_body["address.line1"], distributor_body["address.line2"], distributor_body["address.city"], state_short_code, distributor_body["address.zipCode"]])
        row_number = self.get_table_rows_number()
        table_cells = {
            "Name": distributor_body["name"],
            "Invoice Email": distributor_body["invoiceEmail"],
            "Primary Address": primary_address,
            "Billing Delay": distributor_body["billingDelay"],
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])
        for cell in table_cells_checkbox.keys():
            column = self.get_header_column(cell)
            if table_cells_checkbox[cell] == True:
                self.should_be_present_xpath(f"{self.locators.xpath_table_item(row_number, column)}//span/div")
        checked = sum(1 for value in table_cells_checkbox.values() if value == True)
        self.elements_count_should_be(f"{self.locators.xpath_table}//span/div", check_mark+checked)

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
        self.wait_until_page_loaded()

    def delete_last_distributor(self):
        full_name = self.get_last_table_item_text_by_header("Name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_distributor, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()
