from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.locator import Locator

class DistributorAdminPage(AdminPortalPage):
    distributor_body = {
        "name": None,
        "externalDistributorNumber": None,
        "invoiceEmail": None,
        "address.line1": None,
        "address.line2": None,
        "address.city": None,
        "address.zipCode": None,
        "billingDelay": None,
        "country": None
    }
    table_cells_checkbox = {
        "Process.Fee": True,
        "SupplyForce": True,
        "User Data": True,
        "Agreements": True,
        "Taxes": True,
        "Level": None,
        "Billing Info": True,
        "Bill by all Ship-tos": True
    }

    def create_distributor(self, distributor_body, state, bill_by, checkbox_list):
        check_mark = self.get_element_count(Locator.xpath_check_mark)
        self.click_id(Locator.id_add_button)
        for checkbox in checkbox_list:
            self.select_checkbox_in_dialog_by_name(checkbox)
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(1), distributor_body.pop("country"))
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(2), state)
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(3), bill_by)
        for field in distributor_body.keys():
            self.input_by_name(field, distributor_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        return check_mark

    def check_last_distributor(self, distributor_body, state_short_code, table_cells_checkbox, check_mark):
        primary_address = " ".join([distributor_body["address.line1"], distributor_body["address.line2"], distributor_body["address.city"], state_short_code, distributor_body["address.zipCode"]])
        table_cells = {
            "Name": distributor_body["name"],
            "External Distributor Number": distributor_body["externalDistributorNumber"],
            "Invoice Email": distributor_body["invoiceEmail"],
            "Primary Address": primary_address,
            "Billing Delay": distributor_body["billingDelay"],
            "Country": distributor_body["country"]
        }
        for cell, value in table_cells.items():
            self.check_last_table_item_by_header(cell, value)
        for cell in table_cells_checkbox.keys():
            if table_cells_checkbox[cell]:
                self.get_element_by_xpath(Locator.xpath_check_mark)
        checked = sum(1 for value in table_cells_checkbox.values() if value)
        self.elements_count_should_be(Locator.xpath_check_mark, check_mark+checked)

    def update_last_distributor(self, distributor_body, state, bill_by, checkbox_list, ship_to_level):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, self.get_table_rows_number()))
        for checkbox in checkbox_list:
            self.unselect_checkbox_in_dialog_by_name(checkbox)
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(1), distributor_body.pop("country"))
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(2), state)
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(3), bill_by)
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(4), ship_to_level)
        for field in distributor_body.keys():
            self.input_by_name(field, distributor_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_last_distributor(self):
        full_name = self.get_last_table_item_text_by_header("Name")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()
