from src.pages.customer.customer_portal_page import CustomerPortalPage
from selenium.webdriver.common.keys import Keys

class AllocationCodesPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.allocation_code_body = {
            "name": None,
            "type": None,
            "values": None,
            "isRequired": None,
            "shiptos": None
        }

    def add_allocation_code(self, allocation_code_body):
        self.click_id(self.locators.id_add_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), allocation_code_body.pop("type"))
        self.set_slider(self.locators.xpath_checkbox, allocation_code_body.pop("isRequired"))
        self.manage_shipto(allocation_code_body.pop("shiptos"))
        self.enter_values(allocation_code_body.pop("values"))
        for field in allocation_code_body.keys():
            self.input_by_name(field, allocation_code_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.url_should_be(self.url.get_url_for_env("storeroomlogix.com/allocation-codes", "customer"))
        self.wait_until_page_loaded()

    def enter_values(self, values):
        if (values is not None):
            for value in values:
                element = self.get_element_xpath("//div[@name='values']//input")
                element.send_keys(value)
                element.send_keys(Keys.ENTER)

    def is_required(self, condition):
        if (condition is not None):
            if (condition):
                return "Yes"
            elif (not condition):
                return "No"
            else:
                return None

    def check_allocation_code(self, allocation_code_body):
        table_cells = {
            "Name": allocation_code_body["name"],
            "Type": allocation_code_body["type"],
            "Required": self.is_required(allocation_code_body["isRequired"]),
            "Values": allocation_code_body["values"],
            "Shiptos": allocation_code_body["shiptos"]
        }
        for cell in table_cells.keys():
            self.check_table_item_by_header(self.get_row_of_table_item_by_header(table_cells["Name"], "Name"), cell, table_cells[cell])

    def update_allocation_code(self, current_name, allocation_code_body):
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, self.get_row_of_table_item_by_header(current_name, "Name")))
        self.set_slider(self.locators.xpath_checkbox, allocation_code_body.pop("isRequired"))
        self.manage_shipto(allocation_code_body.pop("shiptos"))
        self.enter_values(allocation_code_body.pop("values"))
        for field in allocation_code_body.keys():
            self.input_by_name(field, allocation_code_body[field])
        self.click_xpath(self.locators.xpath_submit_button)

    def delete_allocation_code(self, current_name):
        current_element_row = self.get_row_of_table_item_by_header(current_name, "Name")
        name = self.get_table_item_text_by_header("Name", current_element_row)
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_allocation_code, current_element_row))
        self.delete_dialog_should_be_about(name)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()