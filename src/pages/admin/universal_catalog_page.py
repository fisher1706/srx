from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.tools import Tools
from src.resources.locator import Locator

class UniversalCatalogPage(AdminPortalPage):
    universal_product_body = {
        "manufacturerPartNumber": None,
        "manufacturer": None,
        "gtin": None,
        "upc": None
    }

    def remapping_to_table_keys(self, body):
        new_body = {
            "UPC": body["upc"],
            "GTIN": body["gtin"],
            "Manufacturer": body["manufacturer"],
            "Manufacturer SKU": body["manufacturerPartNumber"],
            "Distributor Name": None
        }
        return new_body

    def create_universal_product(self, product_body):
        self.click_id(Locator.id_add_button)
        for field in product_body.keys():
            self.input_by_name(field, product_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def update_universal_product(self, product_body, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_edit_button, row))
        for field in product_body.keys():
            self.input_by_name(field, product_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_universal_product(self, row):
        self.click_xpath(Locator.xpath_by_count(Locator.xpath_remove_button, row))
        self.click_xpath(Locator.xpath_dialog+Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def import_universal_catalog(self, elements):
        Tools.generate_csv("universal_catalog.csv", elements)
        self.import_csv(Locator.id_file_upload, "universal_catalog.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()
