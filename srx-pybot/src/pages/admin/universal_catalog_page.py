from src.pages.admin.admin_portal_page import AdminPortalPage

class UniversalCatalogPage(AdminPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.universal_product_body = {
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
            "Manufacturer Part Number": body["manufacturerPartNumber"],
            "Distributor Name": None
        }
        return new_body

    def create_universal_product(self, product_body):
        self.click_id(self.locators.id_add_button)
        for field in product_body.keys():
            self.input_by_name(field, product_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def update_universal_product(self, product_body, row):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_update_utc_and_gtin, row))
        for field in product_body.keys():
            self.input_by_name(field, product_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def delete_universal_product(self, row):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_utc_and_gtin, row))
        self.click_xpath(self.locators.xpath_dialog+self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()