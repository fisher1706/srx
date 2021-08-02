from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class OrderStatusPage(DistributorPortalPage):
    def update_transaction(self, row, quantity=None, status=None):
        if (quantity is not None or status is not None):
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, row))
            if quantity is not None:
                self.input_by_name("reorderQuantity", quantity)
            if status is not None:
                self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), status)
            self.click_xpath(Locator.xpath_submit_button)
            self.wait_until_page_loaded()

    def split_transaction(self, row, quantity):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_split_button, row))
        self.input_by_name("splitFrom", quantity)
        self.click_xpath(Locator.xpath_submit_button)
        self.wait_until_page_loaded()
