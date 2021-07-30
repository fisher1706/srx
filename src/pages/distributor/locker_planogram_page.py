from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class LockerPlanogramPage(DistributorPortalPage):
    def follow_locker_planogram_url(self, customer_id=None, shipto_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        if shipto_id is None:
            shipto_id = self.data.shipto_id
        self.follow_url(self.url.get_url_for_env(f"storeroomlogix.com/customers/{customer_id}/shiptos/{shipto_id}#planogram", "distributor"))

    def create_location_via_planogram(self, door, cell, sku, min_value, max_value):
        self.click_xpath(Locator.xpath_planogram(door, cell))
        self.click_xpath(Locator.xpath_assign_product_planogram)
        self.input_by_name("min", min_value)
        self.input_by_name("max", max_value)
        self.input_data_xpath(sku, f"{Locator.xpath_dialog}{Locator.xpath_select_box}//input")
        self.click_xpath(Locator.xpath_dropdown_sku(sku))
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def open_locker_planogram(self, locker, shipto):
        self.get_element_by_xpath(Locator.xpath_table_row)
        locker_row = self.scan_table(scan_by=locker, column_header="Serial Number", pagination=False)
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_table_row, locker_row)+Locator.xpath_planogram_button)
        self.wait_until_progress_bar_loaded()
        #check device
        text = self.get_element_text(Locator.xpath_dropdown_in_dialog(1))
        if text == f"{locker}":
            self.logger.info(f"Selected Device is {locker} as expected")
        else:
            self.logger.error(f"Selected Device is {text} but should be {locker}")
        current_url = self.driver.current_url
        result = f"{shipto}" in current_url
        if result:
            self.logger.info(f"URL contains shipto id {shipto}")
        else:
            self.logger.error(f"URL contains wrong shipto id {shipto}")

    def assign_smart_shelf_to_locker_door(self, smart_shelf):
        self.click_xpath(Locator.xpath_configure_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), smart_shelf)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_smart_shelf_via_planogram(self, smart_shelf, door_number):
        self.click_xpath(Locator.xpath_configure_button)
        self.get_element_by_xpath(Locator.xpath_dropdown_in_dialog(2))
        self.wait_untill_dropdown_not_empty(Locator.xpath_dropdown_in_dialog(2))
        text = self.get_element_text(Locator.xpath_dropdown_in_dialog(2))
        if text == "":
            for _ in range(3):
                self.click_xpath(Locator.xpath_close_button)
                self.click_xpath(Locator.xpath_configure_button)
                text = self.get_element_text(Locator.xpath_dropdown_in_dialog(2))
                if text != "":
                    break
        self.logger.info(f"Text in dropdown is {text}")
        assert f"{text}" == f"{smart_shelf}", f"Smart shelf {smart_shelf} is NOT assigned to the locker as expected"
        self.logger.info(f"Smart shelf {smart_shelf} is assigned to the locker as expected")

    def check_first_door_is_unavaliable_planogram(self):
        self.click_xpath(Locator.xpath_configure_button)
        self.should_be_disabled_xpath(f"{Locator.xpath_dropdown_in_dialog(2)}//input")
