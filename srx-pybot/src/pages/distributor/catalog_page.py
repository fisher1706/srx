from src.pages.distributor.distributor_portal_page import DistributorPortalPage

class CatalogPage(DistributorPortalPage):
    def __init__(self, activity):
        super().__init__(activity)
        self.product_body = {
            "partSku": None,
            "shortDescription": None,
            "roundBuy": None,
            "lifecycleStatus": None,
            "image": None,
            "longDescription": None,
            "weight": None,
            "height": None,
            "width": None,
            "length": None,
            "issueQuantity": None,
            "packageConversion": None,
            "manufacturerPartNumber": None,
            "manufacturer": None,
            "alternative": None,
            "productLvl1": None,
            "productLvl2": None,
            "productLvl3": None,
            "attribute1": None,
            "attribute2": None,
            "attribute3": None,
            "gtin": None,
            "upc": None,
            "keyword": None,
            "unitName": None
        }

    def create_product(self, product_body):
        self.click_id(self.locators.id_create_button)
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), product_body.pop("lifecycleStatus"))
        for field in product_body.keys():
            self.input_by_name(field, product_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def check_last_product(self, product_body):
        self.open_last_page()
        table_cells = {
            "Distributor SKU": product_body["partSku"],
            "Short Description": product_body["shortDescription"],
            "Round Buy": product_body["roundBuy"],
            "Weight": product_body["weight"],
            "Height": product_body["height"],
            "Width": product_body["width"],
            "Length": product_body["length"],
            "Issue Quantity": product_body["issueQuantity"],
            "Package Conversion": product_body["packageConversion"],
        }
        for cell in table_cells.keys():
            self.check_last_table_item_by_header(cell, table_cells[cell])
        #Not fully checking. Also need to check ALL fields in Details dialog

    def update_last_product(self, product_body):
        self.open_last_page()
        self.click_xpath(self.locators.xpath_by_count(self.locators.title_edit_product, self.get_table_rows_number()))
        self.select_in_dropdown(self.locators.xpath_dropdown_in_dialog(1), product_body.pop("lifecycleStatus"))
        for field in product_body.keys():
            self.input_by_name(field, product_body[field])
        self.click_xpath(self.locators.xpath_submit_button)
        self.dialog_should_not_be_visible()

    def import_product(self, products):
        self.generate_csv("products.csv", products)
        self.import_csv(self.locators.id_file_upload, "products.csv")