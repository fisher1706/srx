from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class CatalogPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)

    def create_product(self, sku, short_description, round_buy, lifecycle_status=None, image="", long_description="", weight="", height="", width="", length="", issue_qantity="", 
                       package_conversion="", manufacturer_part_number="", manufacturer="", alternative="", product_level_1="", product_level_2="", product_level_3="", 
                       attribute_1="", attribute_2="", attribute_3="", gtin="", upc="", keyword=""):
        fields = {
            "partSku": sku,
            "shortDescription": short_description,
            "roundBuy": round_buy,
            "image": image,
            "longDescription": long_description,
            "weight": weight,
            "height": height,
            "width": width,
            "length": length,
            "issueQuantity": issue_qantity,
            "packageConversion": package_conversion,
            "manufacturerPartNumber": manufacturer_part_number,
            "manufacturer": manufacturer,
            "alternative": alternative,
            "productLvl1": product_level_1,
            "productLvl2": product_level_2,
            "productLvl3": product_level_3,
            "attribute1": attribute_1,
            "attribute2": attribute_2,
            "attribute3": attribute_3,
            "gtin": gtin,
            "upc": upc,
            "keyword": keyword
        }
        self.click_id(self.locators.id_create_button)
        for field in fields.keys():
            self.input_by_name(field, fields[field])
        if (lifecycle_status != None):
            self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), lifecycle_status)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_last_product(self, sku, short_description, round_buy, image=None, long_description=None, weight=None, height=None, width=None, length=None, issue_qantity=None, 
                           package_conversion=None, manufacturer_part_number=None, manufacturer=None, alternative=None, product_level_1=None, product_level_2=None, product_level_3=None, 
                           attribute_1=None, attribute_2=None, attribute_3=None, gtin=None, upc=None, keyword=None):
        self.open_last_page()
        detailed_list = {
            "partSku": sku,
            "shortDescription": short_description,
            "roundBuy": round_buy,
            "image": image,
            "longDescription": long_description,
            "weight": weight,
            "height": height,
            "width": width,
            "length": length,
            "issueQuantity": issue_qantity,
            "packageConversion": package_conversion,
            "manufacturerPartNumber": manufacturer_part_number,
            "manufacturer": manufacturer,
            "alternative": alternative,
            "productLvl1": product_level_1,
            "productLvl2": product_level_2,
            "productLvl3": product_level_3,
            "attribute1": attribute_1,
            "attribute2": attribute_2,
            "attribute3": attribute_3,
            "gtin": gtin,
            "upc": upc,
            "keyword": keyword
        }
        table_cells = {
            "Distributor SKU": sku,
            "Short Description": short_description,
            "Round Buy": round_buy,
            "Weight": weight,
            "Height": height,
            "Width": width,
            "Length": length,
            "Issue Quantity": issue_qantity,
            "Package Conversion": package_conversion,
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])
        

    def update_last_product(self, name, number, address1, address2, city, state, code, timezone, contact_email, invoice_email):
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_warehouse, self.get_table_rows_number()))
        self.input_by_name("name", name)
        self.input_by_name("number", number)
        self.input_by_name("address.line1", address1)
        self.input_by_name("address.line2", address2)
        self.input_by_name("address.city", city)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), state)
        self.input_by_name("address.zipCode", code)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(2), timezone)
        self.input_by_name("contactEmail", contact_email)
        self.input_by_name("invoiceEmail", invoice_email)
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def delete_last_product(self):
        warehouse = self.get_last_table_item_text_by_header("Warehouse name")
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_delete_warehouse, self.get_table_rows_number()))
        self.delete_dialog_should_be_about(warehouse)
        self.click_xpath(self.locators.xpath_confirm_button)
        self.dialog_should_not_be_visible()