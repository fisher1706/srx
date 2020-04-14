from src.pages.customer.customer_portal_page import CustomerPortalPage
import time

class AssetsPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.xpath_filter = "//span[text()='Filter']"
        self.xpath_apply = "//span[text()='Apply']"
        self.xpath_asset_card = "//div[data-testid='asset-item']"
        self.xpath_available = "//div[text()='Available']"
        self.xpath_total = "//div[text()='Total']"
        self.xpath_checked_out = "//div[text()='Checked out']"


    def check_all_assets_tab(self, asset, shipto, avaliable, total, checked_out):
        self.click_tab_by_name("All assets")
        self.click_xpath(self.xpath_filter)
        self.select_in_dropdown(self.locators.xpath_select_box, shipto)
        self.click_xpath(self.xpath_apply)
        self.element_should_have_text(f"{self.xpath_available}/../div[2]", f"{avaliable} items")
        self.element_should_have_text(f"{self.xpath_total}/../div[2]", f"{total}")
        self.element_should_have_text(f"{self.xpath_checked_out}/../div[2]", f"{checked_out}")
    
    def check_checked_out_tab(self, asset, shipto, avaliable, total, checked_out):
        self.click_tab_by_name("Checked Out")
        self.click_xpath(self.xpath_filter)
        self.select_in_dropdown(self.locators.xpath_by_count(self.locators.xpath_select_box, 2), shipto)
        #self.select_in_dropdown(self.locators.xpath_select_box, shipto)
        self.click_xpath(self.xpath_apply)
        self.element_should_have_text(f"{self.xpath_checked_out}/../div[2]", f"{checked_out} items")
        self.element_should_have_text(f"{self.xpath_total}/../div[2]", f"{total}")
        self.element_should_have_text(f"{self.xpath_checked_out}/../div[2]", f"{avaliable}")

