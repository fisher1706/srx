from src.pages.customer.customer_portal_page import CustomerPortalPage

class ReorderListPage(CustomerPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.xpath_po_dialog_row = "//div[@data-testid='row']"
        self.xpath_po_dialog_column = "//div[@data-testid='col']"

    def unselect_all(self):
        self.unselect_checkbox(self.locators.xpath_by_count(self.locators.xpath_checkbox, 1))

    def select_by_sku(self, expected_sku):
        replenishment_items_count = self.get_element_count(self.locators.xpath_replenishment_item)
        for index in range(1, replenishment_items_count+1):
            item_xpath = self.locators.xpath_by_count(self.locators.xpath_replenishment_item, index)
            sku_xpath = item_xpath+self.locators.xpath_replenishment_item_sku
            actual_sku = self.get_element_text(sku_xpath)
            if (actual_sku == expected_sku):
                self.select_checkbox(item_xpath+self.locators.xpath_checkbox)
                break
        else:
            self.logger.error("Replenishment item with SKU = '"+str(expected_sku)+"' not found")

    def get_item_xpath_in_po_dialog(self, row, column):
        return "(("+self.locators.xpath_dialog+self.xpath_po_dialog_row+")["+str(row)+"]"+self.xpath_po_dialog_column+")["+str(column)+"]"

    def get_item_text_in_po_dialog(self, row, column):
        item_xpath = self.get_item_xpath_in_po_dialog(row, column)
        return self.get_element_text(item_xpath)

    def check_po_number_in_dialog(self, po_number_body):
        self.click_xpath(self.locators.xpath_submit_quote_button)
        rows_count = self.get_element_count(self.xpath_po_dialog_row)
        for shipto in po_number_body.keys():
            for index in range(1, rows_count+1):
                if (self.get_item_text_in_po_dialog(index, 1) == shipto):
                    po_value = self.get_element_xpath(self.get_item_xpath_in_po_dialog(index, 4)+"//input[@type='text']").get_attribute("value")
                    if (po_number_body[shipto] == po_value):
                        self.logger.info("PO number of '"+str(shipto)+"' shipto is correct")
                    else:
                        self.logger.error("PO number of '"+str(shipto)+"' shipto is incorrect")
                    break
            else:
                self.logger.error("There is no shipto '"+shipto+"' in dialog")
        self.click_xpath(self.locators.xpath_cancel_button)
        self.dialog_should_not_be_visible()

    def submit_replenishment_list_different_po(self, po_number_body):
        self.click_xpath(self.locators.xpath_submit_quote_button)
        self.set_slider(self.locators.xpath_dialog+self.locators.xpath_checkbox, "false")
        rows_count = self.get_element_count(self.xpath_po_dialog_row)
        for shipto in po_number_body.keys():
            for index in range(1, rows_count+1):
                if (self.get_item_text_in_po_dialog(index, 1) == shipto):
                    self.input_data_xpath(po_number_body[shipto], self.get_item_xpath_in_po_dialog(index, 4)+self.locators.xpath_type_text)
                    break
            else:
                self.logger.error("There is no shipto '"+shipto+"' in dialog")
        self.click_xpath(self.locators.xpath_submit_button)
        self.should_be_present_xpath(self.locators.xpath_successfully_submitted_reorder_list)

    def submit_replenishment_list_general_po(self, po_number):
        self.click_xpath(self.locators.xpath_submit_quote_button)
        self.set_slider(self.locators.xpath_dialog+self.locators.xpath_checkbox, "true")
        self.input_data_xpath(po_number, self.locators.xpath_by_count(self.locators.xpath_dialog+self.locators.xpath_type_text, 1))
        self.click_xpath(self.locators.xpath_submit_button)
        self.should_be_present_xpath(self.locators.xpath_successfully_submitted_reorder_list)