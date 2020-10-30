from src.pages.customer.customer_portal_page import CustomerPortalPage
from src.resources.locator import Locator

class ReorderListPage(CustomerPortalPage):
    xpath_po_dialog_row = "//table/tbody/tr"
    xpath_po_dialog_column = "//td"

    def unselect_all(self):
        self.unselect_checkbox(Locator.xpath_by_count(Locator.xpath_checkbox, 1))

    def select_by_sku(self, expected_sku):
        replenishment_items_count = self.get_element_count(Locator.xpath_replenishment_item)
        for index in range(1, replenishment_items_count+1):
            item_xpath = Locator.xpath_by_count(Locator.xpath_replenishment_item, index)
            sku_xpath = item_xpath+Locator.xpath_replenishment_item_sku
            actual_sku = self.get_element_text(sku_xpath)
            if (actual_sku == expected_sku):
                self.select_checkbox(item_xpath+Locator.xpath_checkbox)
                break
        else:
            self.logger.error(f"Replenishment item with SKU = '{expected_sku}' not found")

    def get_item_xpath_in_po_dialog(self, row, column):
        return f"(({Locator.xpath_dialog}{self.xpath_po_dialog_row})[{row}]{self.xpath_po_dialog_column})[{column}]"

    def get_item_text_in_po_dialog(self, row, column):
        item_xpath = self.get_item_xpath_in_po_dialog(row, column)
        return self.get_element_text(item_xpath)

    def check_po_number_in_dialog(self, po_number_body):
        self.click_xpath(Locator.xpath_submit_reorder_list_button)
        rows_count = self.get_element_count(self.xpath_po_dialog_row)
        for shipto in po_number_body.keys():
            self.get_element_by_xpath(f"{Locator.xpath_dialog}//td[text()='{shipto}']")
            for index in range(1, rows_count+1):
                if (self.get_item_text_in_po_dialog(index, 1) == shipto):
                    po_value = self.get_element_by_xpath(f"{self.get_item_xpath_in_po_dialog(index, 4)}//input[@type='text']").get_attribute("value")
                    if (po_number_body[shipto] == po_value):
                        self.logger.info(f"PO number of '{shipto}' shipto is correct")
                    else:
                        self.logger.error(f"PO number of '{shipto}' shipto is incorrect")
                    break
            else:
                self.logger.error(f"There is no shipto '{shipto}' in dialog")
        self.click_xpath(Locator.xpath_cancel_button)
        self.dialog_should_not_be_visible()

    def submit_replenishment_list_different_po(self, po_number_body):
        self.click_xpath(Locator.xpath_submit_reorder_list_button)
        self.set_slider(Locator.xpath_dialog+Locator.xpath_checkbox, "false")
        for shipto in po_number_body.keys():
            self.get_element_by_xpath(f"{Locator.xpath_dialog}//td[text()='{shipto}']")
            rows_count = self.get_element_count(self.xpath_po_dialog_row)
            for index in range(1, rows_count+1):
                text = self.get_item_text_in_po_dialog(index, 1)
                if (self.get_item_text_in_po_dialog(index, 1) == shipto):
                    self.input_data_xpath(po_number_body[shipto], self.get_item_xpath_in_po_dialog(index, 4)+Locator.xpath_type_text)
                    break
            else:
                self.logger.error(f"There is no shipto '{shipto}' in dialog")
        self.click_xpath(Locator.xpath_submit_button)
        self.get_element_by_xpath(Locator.xpath_successfully_submitted_reorder_list)

    def submit_replenishment_list_general_po(self, po_number):
        self.click_xpath(Locator.xpath_submit_reorder_list_button)
        self.set_slider(Locator.xpath_dialog+Locator.xpath_checkbox, "true")
        self.input_data_xpath(po_number, Locator.xpath_by_count(Locator.xpath_dialog+Locator.xpath_type_text, 1))
        self.click_xpath(Locator.xpath_submit_button)
        self.get_element_by_xpath(Locator.xpath_successfully_submitted_reorder_list)