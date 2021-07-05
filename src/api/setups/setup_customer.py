from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.customer_api import CustomerApi
from src.api.distributor.user_api import UserApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupCustomer(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Customer"
        self.options = {
            "expected_status_code": None,
            "user": False,
            "clc": None
        }
        self.customer = Tools.get_dto("customer_dto.json")
        self.customer_id = None
        self.user_email = None
        self.user_id = None

    def setup(self):
        self.set_customer()
        self.set_user()
        self.set_clc()

        response = {
            "customer": self.customer,
            "customer_id": self.customer_id,
            "user_email": self.user_email,
            "user_id": self.user_id
        }

        return copy.deepcopy(response)

    def set_customer(self):
        ca = CustomerApi(self.context)

        self.customer["number"] = Tools.random_string_u()
        self.customer["name"] = Tools.random_string_l()
        self.customer["warehouse"]["id"] = self.context.data.warehouse_id
        self.customer_id = ca.create_customer(copy.deepcopy(self.customer), expected_status_code=self.options["expected_status_code"])
        if (self.customer_id is not None):
            self.context.dynamic_context["delete_customer_id"].append(self.customer_id)

    def set_user(self):
        if (self.options["user"] != False):
            ua = UserApi(self.context)

            self.user_email = self.options["user"] if isinstance(self.options["user"], str) else Tools.random_email()
            self.user_id = ua.create_customer_user(self.customer_id, self.user_email)

    def set_clc(self):
        if (self.options["clc"] is not None):
            sa = SettingsApi(self.context)

            sa.set_customer_level_catalog_flag(self.options["clc"], self.customer_id)