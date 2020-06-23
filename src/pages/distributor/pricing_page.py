from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.resources.tools import Tools

class PricingPage(DistributorPortalPage):
    pricing_body = {
        "Distributor SKU": None,
        "Price": None,
        "UOM": None,
        "Expiration Date": None
    }

    def import_pricing(self, pricing):
        Tools.generate_csv("pricing.csv", pricing)
        self.import_csv(Locator.id_file_upload, "pricing.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()

    def check_price_by_name(self, pricing_body):
        self.scan_table(pricing_body["Distributor SKU"], "Distributor SKU", pricing_body)