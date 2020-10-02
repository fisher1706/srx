from src.api.distributor.customer_api import CustomerApi
from src.api.distributor.warehouse_api import WarehouseApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupCustomer(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Customer"
        self.options = {
            "expected_status_code": None
        }
        self.customer = Tools.get_dto("customer_dto.json")
        self.customer_id = None

    def setup(self):
        self.set_customer()

        response = {
            "customer": self.customer,
            "customer_id": self.customer_id
        }

        return copy.deepcopy(response)

    def set_customer(self):
        ca = CustomerApi(self.context)

        self.customer["number"] = Tools.random_string_l()
        self.customer["name"] = Tools.random_string_l()
        self.customer["warehouse"]["id"] = self.context.data.warehouse_id
        self.customer_id = ca.create_customer(copy.deepcopy(self.customer), expected_status_code=self.options["expected_status_code"])
        if (self.customer_id is not None):
            self.context.dynamic_context["delete_customer_id"].append(self.customer_id)