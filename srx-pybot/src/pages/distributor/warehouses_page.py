from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class WarehousesPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def create_warehouse(self, name, number, address1, address2, city, state, code, timezone, contact_email, invoice_email):
        self.click_id(self.locators.id_create_button)
        self.input_by_name("name", name)
        self.input_by_name("number", number)
        self.input_by_name("address.line1", address1)
        self.input_by_name("address.line2", address2)
        self.input_by_name("address.city", city)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), state)
        self.input_by_name("address.zipCode", code)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), timezone)
        self.input_by_name("contactEmail", contact_email)
        self.input_by_name("invoiceEmail", invoice_email)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_last_warehouse(self, name, number, timezone, address, contact_email, invoice_email):
        self.check_last_table_item_by_header("Warehouse name", name)
        self.check_last_table_item_by_header("Warehouse number", number)
        self.check_last_table_item_by_header("Timezone", timezone)
        self.check_last_table_item_by_header("Warehouse address", address) 
        self.check_last_table_item_by_header("Contact email", contact_email)
        self.check_last_table_item_by_header("Invoice email", invoice_email)

    def update_last_warehouse(self, name, number, address1, address2, city, state, code, timezone, contact_email, invoice_email):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_warehouse, self.get_table_rows_number()))
        self.input_by_name("name", name)
        self.input_by_name("number", number)
        self.input_by_name("address.line1", address1)
        self.input_by_name("address.line2", address2)
        self.input_by_name("address.city", city)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), state)
        self.input_by_name("address.zipCode", code)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), timezone)
        self.input_by_name("contactEmail", contact_email)
        self.input_by_name("invoiceEmail", invoice_email)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_warehouse(self):
        warehouse = self.get_last_table_item_text_by_header("Warehouse name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_warehouse, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(warehouse)
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()