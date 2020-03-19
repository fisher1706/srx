from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.tools import Tools
import time
import random

class FeesPage(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.fee_price = {
            "Level 1": None,
            "Level 2": None,
            "Level 3": None
        }

    def set_fee_price(self, fee_price):
        row = 0
        self.click_tab_by_name("ShipTo Fees")
        for field in fee_price.keys():
            row +=1
            self.input_inline_xpath(fee_price[field], f"{self.locators.xpath_table_item(row, 2)}")

    def check_fee_price(self, fee_price):
        row = 0
        self.page_refresh
        self.wait_until_page_loaded
        for field in fee_price.keys():
            row +=1
            self.check_table_item_by_header(row, "Price", f"${fee_price[field]}.00")

    def undo(self, fee_price):
        for field in fee_price.keys():
            self.wait_until_page_loaded
            self.click_xpath(self.locators.title_undo)

