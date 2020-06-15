from src.pages.customer.customer_portal_page import CustomerPortalPage
import time

class AssetsPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.xpath_filter = "//span[text()='Filter']"
        self.xpath_apply = "//span[text()='Apply']"
        self.xpath_asset_card = "//div[@data-testid='asset-item']"
        self.xpath_available = "//div[text()='Available']"
        self.xpath_total = "//div[text()='Total']"
        self.xpath_checked_out = "//div[text()='Checked out']"
        self.xpath_user = "//div[text()='User']"
        self.xpath_return_requested_text = "//div[text()='Asset return has been requested']"
        self.xpath_sku_input = "//label[text()='Distributor SKU']/../div/input"
        #self.xpath_empty_list = "//div[text()='List of checked out assets is empty.']"


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
        self.select_in_dropdown(self.locators.xpath_select_box, shipto)
        self.click_xpath(self.xpath_apply)
        if (checked_out == 1):
            self.element_should_have_text(f"{self.xpath_checked_out}/../div[2]", f"1 item")
        else:
            self.element_should_have_text(f"{self.xpath_checked_out}/../div[2]", f"{checked_out} items")
        self.element_should_have_text(f"{self.xpath_total}/../div[2]", f"{total}")
        self.element_should_have_text(f"{self.xpath_available}/../div[2]", f"{avaliable}")
        text = self.get_element_text(f"{self.xpath_user}/../div[2]/a")
        self.element_should_have_text(f"{self.xpath_user}/../div[2]/a", f"{self.variables.customer_email} {self.variables.customer_email} {self.variables.customer_email}")

    def checked_out_tab_should_not_contain(self, asset):
        self.click_tab_by_name("Checked Out")
        self.click_xpath(self.xpath_filter)
        self.input_data_xpath(asset, self.xpath_sku_input)
        self.click_xpath(self.xpath_apply)
        self.elements_count_should_be(self.xpath_asset_card, 0, time=5)

    def ping_to_return_last_asset(self):
        self.click_tab_by_name("Checked Out")
        self.click_xpath(f"{self.locators.xpath_ping_to_return}")
        self.wait_until_progress_bar_loaded()
        self.elements_count_should_be(f"({self.xpath_asset_card})[1]{self.xpath_return_requested_text}", 1)


