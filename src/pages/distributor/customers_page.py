from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class CustomersPage(DistributorPortalPage):
    customer_body = {
        "name": None,
        "number": None,
        "customerType": None,
        "marketType": None,
        "warehouse": None,
        "notes": None,
        "supplyForce": None
    }

    def create_customer(self, customer_body):
        self.get_element_by_xpath(Locator.xpath_table_row)
        start_number_of_rows = self.get_table_rows_number()
        self.click_id(Locator.id_item_action_customer_add)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), customer_body.pop("customerType"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), customer_body.pop("marketType"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(3), customer_body.pop("warehouse"))
        self.set_slider(Locator.xpath_dialog+Locator.xpath_checkbox, customer_body.pop("supplyForce"))
        for field in customer_body.keys():
            self.input_by_name(field, customer_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
        self.elements_count_should_be(Locator.xpath_table_row, start_number_of_rows+1)

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

    def update_last_customer(self, customer_body):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, self.get_table_rows_number())+Locator.xpath_customer_info_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), customer_body.pop("customerType"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), customer_body.pop("marketType"))
        self.set_slider(Locator.xpath_checkbox, customer_body.pop("supplyForce"))
        for field in customer_body.keys():
            self.input_by_name(field, customer_body[field])
        self.click_xpath(Locator.xpath_submit_button)

    def click_on_customer_setup_wizard_button(self):
        self.click_xpath("//button/span[text()='Customer setup wizard']")

    def check_customer_setup_wizard_button(self):
        self.wait_until_page_loaded()
        if (self.get_element_count("//button/span[text()='Customer setup wizard']") == 0):
            self.logger.info(f"Button is hidden for user")
        else:
            self.logger.error(f"Create setup wizard button is enabled for user")
            
    def select_warehouse(self):
        self.click_xpath("/html/body/div/main/div/div[2]/div/div[2]/div/div[3]/div/div[1]/div/div[1]/div/div[5]/div/button") 
        self.click_xpath(Locator.xpath_next)
    
    def add_customer_info(self,customer_body):
        self.wait_until_page_loaded()
        self.get_element_by_xpath("//input[@name='name']").send_keys(customer_body.pop("name"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), customer_body.pop("customerType"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), customer_body.pop("marketType"))
        self.click_xpath(Locator.xpath_next)

    def add_customer_portal_user(self,email):
        self.wait_until_page_loaded()
        self.select_checkbox(Locator.xpath_checkbox)
        self.get_element_by_xpath("//input[@value='']").send_keys(email)

    def click_complete(self):
        self.click_xpath(Locator.xpath_complete_button)
        self.wait_until_page_loaded()

    def click_next(self):
        self.click_xpath(Locator.xpath_next)
        self.wait_until_page_loaded()

    def check_customer_portal_user(self, expected_email):
        self.wait_until_page_loaded()
        self.check_last_table_item_by_header("Email",expected_email)

    def check_settings_list_rules(self,expected_email):
        self.wait_until_page_loaded()
        self.click_xpath("//span[text()='Replenishment list rules']")
        self.get_element_by_xpath("//input[@name='email']").get_attribute("value")  == expected_email 
    
    def check_settings(self,expected_text):
        self.click_xpath("//span[text()='Lot & Serialization Settings']")
        self.get_element_by_xpath("//input[@name='daysUntilExpirationAlarm']").get_attribute("value") == expected_text

    def change_automation_settings(self):
        self.click_xpath("//span[text()='Submit Immediately']")
        self.click_xpath("//span[text()='Auto-submit as Order']")
        self.click_xpath(Locator.xpath_next)
        self.wait_until_page_loaded()

    def change_reorder_list_settings(self,email):
        self.wait_until_page_loaded()
        self.click_xpath("//span[text()='Use defaults']")
        self.clear_xpath("//input[@name='email']")
        self.get_element_by_xpath("//input[@name='email']").send_keys(email)
        self.click_xpath(Locator.xpath_next)
        self.wait_until_page_loaded()

    def change_reorder_lot_serialization_settings(self,number):
        self.wait_until_page_loaded()
        self.click_xpath("//span[text()='Expiration Alarm']")
        self.clear_xpath("//input[@name='daysUntilExpirationAlarm']")
        self.get_element_by_xpath("//input[@name='daysUntilExpirationAlarm']").send_keys(number)
        self.click_xpath(Locator.xpath_complete_button)
        self.wait_until_page_loaded()

    def delete_last_customer(self):
        name = self.get_last_table_item_text_by_header("Name")
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(name)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()