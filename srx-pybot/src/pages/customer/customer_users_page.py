from src.pages.customer.customer_portal_page import CustomerPortalPage

class CustomerUsersPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.customer_user_body = {
            "firstName": None,
            "lastName": None,
            "email": None,
            "role": None,
            "shiptos": None
        }

    def create_customer_user(self, customer_user_body):
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), customer_user_body.pop("role"))
        self.manage_shipto(customer_user_body.pop("shiptos"), self.locators.xpath_dialog)
        for field in customer_user_body.keys():
            self.input_by_name(field, customer_user_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(self.locators.xpath_table_row, start_number_of_rows+1)

    def check_last_customer_user(self, customer_user_body):
        self.open_last_page()
        table_cells = {
            "Email": customer_user_body["email"],
            "First Name": customer_user_body["firstName"],
            "Last Name": customer_user_body["lastName"],
            "Security Group": customer_user_body["role"],
            "Shiptos": customer_user_body["shiptos"]
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def update_last_customer_user(self, customer_user_body):
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, self.get_table_rows_number()))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), customer_user_body.pop("role"))
        self.manage_shipto(customer_user_body.pop("shiptos"), self.locators.xpath_dialog)
        for field in customer_user_body.keys():
            self.input_by_name(field, customer_user_body[field])
        self.click_xpath(self.locators.xpath_submit_button)

    def delete_last_customer_user(self):
        full_name = self.get_last_table_item_text_by_header("First Name")
        full_name += " " + self.get_last_table_item_text_by_header("Last Name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_user, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
