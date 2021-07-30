from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.resources.tools import Tools

class CribcrawlPage(DistributorPortalPage):
    def follow_cribcrawl_url(self, customer_id=None, shipto_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        if shipto_id is None:
            shipto_id = self.data.shipto_id
        self.follow_url(self.url.get_url_for_env(f"storeroomlogix.com/customers/{customer_id}/shiptos/{shipto_id}#cribcrawl-list", "distributor"))

    def check_last_cribcrawl(self, cribcrawl_body):
        self.open_last_page()
        table_cells = {
            "Distributor SKU": cribcrawl_body["sku"],
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])

    def import_cribcrawl(self, cribcrawls):
        Tools.generate_csv("cribcrawls.csv", cribcrawls)
        self.import_csv(Locator.id_file_upload, "cribcrawls.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()
