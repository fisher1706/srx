from src.api.customer.checkout_group_api import CheckoutGroupApi
from src.api.customer.customer_user_api import CustomerUserApi
from src.resources.tools import Tools
from src.api.setups.base_setup import BaseSetup
import copy

class SetupCheckoutGroup(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Checkout Group"
        self.options = {
            "email": None,
        }
        self.group = None

    def setup(self):
        self.set_checkout_group()

        response = {
            "group": self.group
        }

        return copy.deepcopy(response)

    def set_checkout_group(self):
        cga = CheckoutGroupApi(self.context)
        ca = CustomerUserApi(self.context)
        customer_user_id = ca.get_customer_users()[0]["id"]
        checkout_group_dto = {
            "name": "Name " + Tools.random_string_l(),
            "email": Tools.random_email() if self.options["email"] is None else self.options["email"],
            "owner": {
                "id": customer_user_id
            },
        }
        self.group = cga.create_checkout_group(checkout_group_dto)
        self.context.dynamic_context["delete_checkout_group_id"].append(self.group["id"])