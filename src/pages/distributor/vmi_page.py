from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.resources.tools import Tools

class VmiPage(DistributorPortalPage):
    location_body = {
        "sku": None,
        "orderingConfig.currentInventoryControls.min": None,
        "orderingConfig.currentInventoryControls.max": None,
        "attributeName1": None,
        "attributeValue1": None,
        "customerSku": None,
        "type": None
    }
    xpath_button_bulk_operations = f"{Locator.xpath_button_type}//span[text()='Bulk operations']"

    def follow_location_url(self, customer_id=None, shipto_id=None):
        if customer_id is None:
            customer_id = self.data.customer_id
        if shipto_id is None:
            shipto_id = self.data.shipto_id
        self.follow_url(f"{self.url.distributor_portal}/customers/{customer_id}/shiptos/{shipto_id}#vmi-list")

    def create_location(self, location_body):
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown_via_input(Locator.xpath_dropdown_in_dialog(1), location_body.pop("sku"), span=True)
        for field in location_body.keys():
            self.input_by_name(field, location_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.wait_until_page_loaded()

    def check_last_location(self, location_body):
        self.open_last_page()
        table_cells = {
            "Distributor SKU": location_body["sku"],
        }
        for cell, value in table_cells.items():
            self.check_last_table_item_by_header(cell, value)

    def import_location(self, locations):
        Tools.generate_csv("locations.csv", locations)
        self.click_id(Locator.id_item_action_import)
        self.import_csv(Locator.id_file_upload, "locations.csv")
        self.get_element_by_xpath(Locator.xpath_successfully_imported_msg)
        self.wait_until_page_loaded()
