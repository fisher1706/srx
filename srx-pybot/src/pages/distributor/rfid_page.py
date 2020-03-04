from src.pages.distributor.distributor_portal_page import DistributorPortalPage
import time

class RfidPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def select_shipto_sku(self, shipto, sku):
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), shipto)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), sku)