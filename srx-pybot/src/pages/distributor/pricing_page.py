from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class PricingPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.pricing_body = {
            "SKU": None,
            "Price": None,
            "UOM": None,
            "Expiration Date": None
        }

    def import_pricing(self, pricing):
        self.generate_csv("pricing.csv", pricing)
        self.import_csv(self.locators.id_file_upload, "pricing.csv")
        self.should_be_present_xpath(self.locators.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()

    def check_price_by_name(self, pricing_body):
        self.scan_table(pricing_body["SKU"], "SKU", pricing_body)