from src.pages.distributor.distributor_portal_page import DistributorPortalPage
import time

class LockerPlanogramPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def follow_locker_planogram_url(self, customer_id=None, shipto_id=None):
        if (customer_id is None):
            customer_id = self.variables.customer_id
        if (shipto_id is None):
            shipto_id = self.variables.shipto_id
        self.follow_url(self.url.get_url_for_env(f"storeroomlogix.com/customers/{customer_id}/shiptos/{shipto_id}#planogram", "distributor"), hide_intercom=True)
        
    def create_location_via_planogram(self, door, cell, sku, min_value, max_value):
        self.click_xpath(self.locators.xpath_planogram(door, cell))
        self.click_xpath(self.locators.xpath_assign_product_planogram)
        self.input_data_xpath(sku, f"{self.locators.xpath_dialog}{self.locators.xpath_select_box}//input")
        self.wait_until_dropdown_list_loaded(1)
        self.click_xpath(self.locators.xpath_dropdown_list_item)
        self.input_by_name("min", min_value)
        self.input_by_name("max", max_value)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
    
    def open_locker_planogram(self, locker, shipto):
        self.open_last_page()
        locker_row = self.get_row_of_table_item_by_header(locker, "Serial Number")
        self.click_xpath(self.locators.xpath_by_count(self.locators.xpath_table_row, locker_row)+self.locators.title_switch_locker_planogram)
        self.wait_until_progress_bar_loaded()
        #check device
        text = self.get_element_text(self.locators.xpath_dropdown_in_dialog(1))
        if (text == f"LOCKER - {locker}"):
            self.logger.info(f"Selected Device is {locker} as expected")
        else:
            self.logger.error(f"Selected Device is {text} but should be {locker}")
        current_url = self.driver.current_url
        result = f"{shipto}" in current_url
        if (result is True): 
            self.logger.info(f"URL contains shipto id {shipto}")
        else: 
            self.logger.error(f"URL contains wrong shipto id {shipto}")
    
    def assign_smart_shelf_to_locker_door(self, smart_shelf):
        self.wait_until_progress_bar_loaded()
        self.click_xpath(self.locators.title_configure_door_number)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), smart_shelf)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
    
    def check_smart_shelf_via_planogram(self, smart_shelf, door_number):
        self.wait_until_progress_bar_loaded()
        self.click_xpath(self.locators.title_configure_door_number)
        text = self.get_element_text(self.locators.xpath_dropdown_in_dialog(2))
        if (text == smart_shelf):
            self.logger.info(f"Smart shelf {smart_shelf} is assigned to the locker as expected")
        else:
            self.logger.error(f"Smart shelf {smart_shelf} is NOT assigned to the locker as expected")

    def check_first_door_is_unavaliable_planogram(self):
        self.wait_until_progress_bar_loaded()
        self.click_xpath(self.locators.title_configure_door_number)
        self.should_be_disabled_xpath(f"{self.locators.xpath_dropdown_in_dialog(2)}//input")