from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class UsageHistoryPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.usage_history_body = {
            "Order Number": None,
            "Customer Number": None,
            "ShipTo Number": None,
            "ShipTo Name": None,
            "Part SKU": None,
            "Quantity": None,
            "Date": None,
        }

    def follow_usage_history_url(self):
        self.follow_url(self.url.get_url_for_env("storeroomlogix.com/customers/"+self.variables.customer_id+"#usage-history", "distributor"))

    def import_usage_history(self, usage_history):
        self.generate_csv("usage_history.csv", usage_history)
        self.import_csv(self.locators.id_file_upload, "usage_history.csv")
        self.should_be_present_xpath(self.locators.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()

    def check_last_usage_history(self, usage_history_body):
        self.open_last_page()
        for cell in usage_history_body.keys():
            self.check_last_table_item_by_header(cell, usage_history_body[cell])