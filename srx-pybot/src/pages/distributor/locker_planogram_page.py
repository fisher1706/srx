from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class LockerPlanogramPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def follow_locker_planogram_url(self, customer_id=None, shipto_id=None):
        if (customer_id is None):
            customer_id = self.variables.customer_id
        if (shipto_id is None):
            shipto_id = self.variables.shipto_id
        self.follow_url(self.url.get_url_for_env("storeroomlogix.com/customers/"+str(customer_id)+"/shiptos/"+str(shipto_id)+"#locker-planogram", "distributor"), hide_intercom=True)
        
    def create_location_via_planogram(self, door, cell, sku, min_value, max_value):
        self.click_xpath(self.locators.xpath_planogram(door, cell))
        self.click_xpath(self.locators.xpath_assign_product_planogram)
        self.input_data_xpath(sku, self.locators.xpath_dialog+self.locators.xpath_select_box+"//input")
        self.wait_until_dropdown_list_loaded(1)
        self.click_xpath(self.locators.xpath_dropdown_list_item)
        self.input_by_name("min", min_value)
        self.input_by_name("max", max_value)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()