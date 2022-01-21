from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator

class OrderStatusPage(DistributorPortalPage):
    def update_transaction(self, row, reorder_quantity=None, shipped_quantity=None, status=None):
        if (reorder_quantity is not None or status is not None):
            self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, row))
            if reorder_quantity is not None:
                self.input_by_name("reorderQuantity", reorder_quantity)
            if status is not None:
                self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), status)
            if shipped_quantity is not None:
                self.input_by_name("shippedQuantity", shipped_quantity)
            self.click_xpath(Locator.xpath_submit_button)
            self.dialog_should_not_be_visible()
            self.wait_until_page_loaded()

    def split_transaction(self, row, quantity):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_split_button, row))
        self.input_by_name("splitFrom", quantity)
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()
