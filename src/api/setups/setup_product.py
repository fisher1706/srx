import random
import copy
from src.api.distributor.product_api import ProductApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools

class SetupProduct(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "Product"
        self.options = {
            "product": None,
            "sku": None,
            "serialized": None,
            "lot": None,
            "package_conversion": None,
            "asset": None,
            "round_buy": None,
            "issue_quantity": None
        }
        self.product = Tools.get_dto("product_dto.json")
        self.product_id = None
        self.expected_status_code = None

    def setup(self, expected_status_code=None):
        self.expected_status_code = expected_status_code
        self.set_product()
        return copy.deepcopy(self.product)

    def set_product(self):
        pa = ProductApi(self.context)
        if self.options["product"] is None:
            if self.options["sku"] is None:
                self.product["partSku"] = Tools.random_string_u(18)
            else:
                self.product["partSku"] = self.options["sku"]
            self.product["shortDescription"] = f"{self.product['partSku']} - short description"
            self.product["assetFlag"] = bool(self.options["asset"])
            if bool(self.options["asset"]):
                self.product["roundBuy"] = 1 if self.options["round_buy"] is None else self.options["round_buy"]
            else:
                self.product["roundBuy"] = random.choice(range(2, 100)) if self.options["round_buy"] is None else self.options["round_buy"]
            self.product["serialized"] = self.options["serialized"]
            self.product["lot"] = self.options["lot"]
            self.product["packageConversion"] = self.options["package_conversion"]
            self.product["issueQuantity"] = self.options["issue_quantity"]
        else:
            self.product = self.options["product"]
        self.product_id = pa.create_product(copy.deepcopy(self.product), expected_status_code=self.expected_status_code)
        if self.expected_status_code is None:
            self.product["packageConversion"] = pa.get_product(self.product["partSku"])[0]["calculatedPackageConversion"]
        self.product["id"] = self.product_id
