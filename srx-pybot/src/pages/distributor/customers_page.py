from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class CustomersPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.customer_body = {
            "name": None,
            "number": None,
            "customerType": None,
            "marketType": None,
            "warehouse": None,
            "notes": None,
            "supplyForce": None
        }

    def create_customer(self, customer_body):
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), customer_body.pop("customerType"))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), customer_body.pop("marketType"))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(3), customer_body.pop("warehouse"))
        self.set_slider(self.locators.xpath_dialog+self.locators.xpath_checkbox, customer_body.pop("supplyForce"))
        for field in customer_body.keys():
            self.input_by_name(field, customer_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(self.locators.xpath_table_row, start_number_of_rows+1)

    def check_last_customer(self, customer_body):
        self.open_last_page()
        table_cells = {
            "Name": customer_body["name"],
            "Number": customer_body["number"],
            "Warehouse": customer_body["warehouse"],
            "Customer Type": customer_body["customerType"],
            "Market Type": customer_body["marketType"]
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def open_customer_users(self, row):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_manage_customer_users, row))

    def open_last_customer_users(self):
        self.open_customer_users(self.get_table_rows_number())

    def update_last_customer(self, customer_body):
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, self.get_table_rows_number())+self.locators.title_customer_info)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), customer_body.pop("customerType"))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), customer_body.pop("marketType"))
        self.set_slider(self.locators.xpath_checkbox, customer_body.pop("supplyForce"))
        for field in customer_body.keys():
            self.input_by_name(field, customer_body[field])
        self.click_xpath(self.locators.xpath_submit_button)

    def delete_last_customer(self):
        name = self.get_last_table_item_text_by_header("Name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_customer, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()