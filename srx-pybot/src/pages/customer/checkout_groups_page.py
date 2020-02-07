from src.pages.customer.customer_portal_page import CustomerPortalPage
import time

class CheckoutGroupsPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.checkout_group_body = {
            "name": None,
            "email": None
        }
        self.id_associate = "item-action-associate"

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

    def assign_shipto(self, shipto_number):
        self.click_id(self.id_associate)
        for index in range(1, self.get_element_count(self.locators.xpath_dialog+self.locators.xpath_table_row)+1):
            if(self.get_element_text(self.locators.xpath_table_item_in_dialog(index, 1)) == str(shipto_number)):
                self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_dialog+self.locators.xpath_table_row+self.locators.xpath_button_type, index))
                break
        else:
            self.logger.error("There is no shipto '"+str(shipto_number)+"'")
        self.click_xpath(self.locators.xpath_button_save)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_assigned_shipto(self, shipto_body, row):
        table_cells = {
            "Shipto Number": shipto_body["number"],
            "Shipto Name": shipto_body["name"],
            "Address": [shipto_body["address"]["zipCode"], shipto_body["address"]["line1"], shipto_body["address"]["line2"], shipto_body["address"]["city"]],
            "Distributor": self.variables.distributor_name
        }
        for cell in table_cells.keys():
            self.check_table_item_by_header(row, cell, table_cells[cell])

    def unassign_shipto(self, row):
        shipto_number = self.get_table_item_text_by_header("Shipto Number", row)
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, row)+self.locators.title_delete_associated_shipto)
        self.delete_dialog_should_be_about(shipto_number)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def assign_user(self, user_email):
        self.click_id(self.id_associate)
        for index in range(1, self.get_element_count(self.locators.xpath_dialog+self.locators.xpath_table_row)+1):
            if(self.get_element_text(self.locators.xpath_table_item_in_dialog(index, 4)) == str(user_email)):
                self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_dialog+self.locators.xpath_table_row+self.locators.xpath_button_type, index))
                break
        else:
            self.logger.error("There is no shipto '"+str(user_email)+"'")
        self.click_xpath(self.locators.xpath_button_save)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_assigned_user(self, user_body, row):
        table_cells = {
            "First Name": user_body["firstName"],
            "Last Name": user_body["lastName"],
            "Email": user_body["email"]
        }
        for cell in table_cells.keys():
            self.check_table_item_by_header(row, cell, table_cells[cell])

    def unassign_user(self, row):
        full_name = self.get_last_table_item_text_by_header("First Name")
        full_name += " " + self.get_last_table_item_text_by_header("Last Name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, row)+self.locators.title_delete_associated_user)
        self.delete_dialog_should_be_about(full_name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()