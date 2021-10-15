import random
import copy
from src.api.customer.customer_product_api import CustomerProductApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools

class SetupCustomerProduct(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "Product"
        self.options = {
            "product": None,
            "package_conversion": None,
            "asset": None,
            "round_buy": None,
            "issue_quantity": None,
            "supplier_id": None
        }
        self.product = Tools.get_dto("customer_product_dto.json")
        self.product_id = None

    def setup(self):
        self.set_product()
        return copy.deepcopy(self.product)

    def set_product(self):
        cpa = CustomerProductApi(self.context)
        if self.options["product"] is None:
            self.product["partSku"] = Tools.random_string_u(18)
            self.product["customerSku"] = self.product["partSku"]
            self.product["shortDescription"] = f"{self.product['partSku']} - short description"
            self.product["assetFlag"] = bool(self.options["asset"])
            if bool(self.options["asset"]):
                self.product["roundBuy"] = 1 if self.options["round_buy"] is None else self.options["round_buy"]
            else:
                self.product["roundBuy"] = random.choice(range(2, 100)) if self.options["round_buy"] is None else self.options["round_buy"]
            self.product["packageConversion"] = self.options["package_conversion"]
            self.product["issueQuantity"] = self.options["issue_quantity"]
            self.product["distributor"]["id"] = self.options["supplier_id"]
        else:
            self.product = self.options["product"]
        self.product_id = cpa.create_product(copy.deepcopy(self.product), self.options["supplier_id"])
        self.product["id"] = self.product_id
