from src.pages.customer.customer_portal_page import CustomerPortalPage

class CheckoutGroupsPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.checkout_group_body = {
            "name": None,
            "email": None
        }

    def create_checkout_group(self, checkout_group_body):
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(self.locators.id_add_button)
        for field in checkout_group_body.keys():
            self.input_by_name(field, checkout_group_body[field])
        self.click_xpath(self.locators.xpath_dropdown_in_dialog(1))
        self.click_xpath(self.locators.xpath_dropdown_list_item+"/div")
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(self.locators.xpath_table_row, start_number_of_rows+1)

    def check_new_checkout_group(self, checkout_group_body, row, owner=None, shipto=None):
        table_cells = {
            "Checkout Group Name": checkout_group_body["name"],
            "Checkout Group Email": checkout_group_body["email"],
            "Owner": owner,
            "Associated Shipto": shipto
        }
        for cell in table_cells.keys():
            self.check_table_item_by_header(row, cell, table_cells[cell])

    def update_new_checkout_group(self, checkout_group_body, row):
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, row))
        self.click_xpath(self.locators.xpath_dropdown_in_dialog(1))
        self.click_xpath(self.locators.xpath_dropdown_list_item+"/div[last()]")
        for field in checkout_group_body.keys():
            self.input_by_name(field, checkout_group_body[field])
        self.click_xpath(self.locators.xpath_submit_button)

    def delete_new_checkout_group(self, row):
        full_name = self.get_table_item_text_by_header("Checkout Group Name", row)
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, row)+self.locators.title_delete_checkout_group)
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
