from src.pages.distributor.distributor_portal_page import DistributorPortalPage
from src.resources.locator import Locator
from src.api.distributor.warehouse_api import WarehouseApi

class WarehousesPage(DistributorPortalPage):
    warehouse_body = {
        "name": None,
        "number": None,
        "address.line1": None,
        "address.line2": None,
        "address.city": None,
        "address.zipCode": None,
        "state": None,
        "contactEmail": None,
        "invoiceEmail": None,
        "timezone": None
    }

    def create_warehouse(self, warehouse_body):
        wa = WarehouseApi(self.context)
        start_number_of_rows = wa.get_warehouses()["totalElements"]
        self.click_id(Locator.id_add_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), warehouse_body.pop("state"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), warehouse_body.pop("timezone"))
        for field in warehouse_body.keys():
            self.input_by_name(field, warehouse_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()
        self.last_page(10)
        self.get_element_by_xpath(Locator.xpath_get_row_by_index(start_number_of_rows%10))

    def check_last_warehouse(self, warehouse_body):
        table_cells = {
            "Warehouse name": warehouse_body["name"],
            "Warehouse number": warehouse_body["number"],
            "Timezone": warehouse_body["timezone"],
            "Warehouse address": [warehouse_body["address.zipCode"], warehouse_body["address.line1"], warehouse_body["address.line2"], warehouse_body["address.city"]],
            "Contact email": warehouse_body["contactEmail"],
            "Invoice email": warehouse_body["invoiceEmail"]
        }
        for cell, value in table_cells.items():
            self.check_table_item(value, header=cell, last=True)

    def update_last_warehouse(self, warehouse_body):
        self.click_xpath(Locator.xpath_last_role_row+Locator.xpath_edit_button)
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(1), warehouse_body.pop("state"))
        self.select_in_dropdown(Locator.xpath_dropdown_in_dialog(2), warehouse_body.pop("timezone"))
        for field in warehouse_body.keys():
            self.input_by_name(field, warehouse_body[field])
        self.click_xpath(Locator.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_warehouse(self, value):
        self.click_xpath(Locator.xpath_last_role_row+Locator.xpath_remove_button)
        self.delete_dialog_should_be_about(value)
        self.click_xpath(Locator.xpath_confirm_button)
        self.dialog_should_not_be_visible()
