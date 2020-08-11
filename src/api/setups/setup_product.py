from src.api.distributor.product_api import ProductApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import random
import copy

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
            "asset": None
        }
        self.product = Tools.get_dto("product_dto.json")

    def setup(self, expected_status_code=None):
        self.expected_status_code = expected_status_code
        self.set_product()

        return copy.deepcopy(self.product)

    def set_product(self):
        pa = ProductApi(self.context)
        if (self.options["product"] is None):
            if (self.options["sku"] is None):
                self.product["partSku"] = Tools.random_string_u(18)
            else:
                self.product["partSku"] = self.options["sku"]
            self.product["shortDescription"] = f"{self.product['partSku']} - short description"
            self.product["roundBuy"] = random.choice(range(2, 100))
            self.product["assetFlag"] = bool(self.options["asset"])
            self.product["serialized"] = self.options["serialized"]
            self.product["lot"] = self.options["lot"]
            self.product["packageConversion"] = self.options["package_conversion"]
        else:
            self.product = self.options["product"]

        self.id = pa.create_product(copy.deepcopy(self.product), expected_status_code=self.expected_status_code)
        self.product["id"] = self.id