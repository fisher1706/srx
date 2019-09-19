from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class CustomersPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def create_customer(self, name, number, customer_type, market_type, warehouse, notes, supply_force):
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(self.locators.id_create_button)
        self.input_by_name("name", name)
        self.input_by_name("number", number)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), customer_type)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), market_type)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(3), warehouse)
        self.input_by_name("notes", notes)
        self.set_slider(self.locators.xpath_dialog+self.locators.xpath_checkbox, supply_force)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.new_element_appears_in_table(start_number_of_rows+1)

    def check_last_customer(self, name, number, customer_type, market_type, warehouse):
        self.check_last_table_item_by_header("Name", name)
        self.check_last_table_item_by_header("Number", number)
        self.check_last_table_item_by_header("Warehouse", warehouse)
        self.check_last_table_item_by_header("Customer Type", customer_type) 
        self.check_last_table_item_by_header("Market Type", market_type)

    def update_customer(self, name, number, customer_type, market_type, notes, supply_force):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_customer_info, self.get_table_rows_number()))
        self.input_by_name("name", name)
        self.input_by_name("number", number)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), customer_type)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), market_type)
        self.input_by_name("notes", notes)
        self.set_slider(self.locators.xpath_checkbox, supply_force)
        self.click_xpath(self.locators.xpath_submit_button)

    def delete_last_customer(self):
        name = self.get_last_table_item_text_by_header("Name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_customer, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()