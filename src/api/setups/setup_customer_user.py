from src.api.customer.customer_user_api import CustomerUserApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupCustomerUser(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Customer User"
        self.options = {
            "email": None,
            "group": None
        }
        self.user = Tools.get_dto("customer_user_dto.json")
        self.user_id = None

    def setup(self):
        self.set_user()

        response = {
            "user": self.user,
            "user_id": self.user_id
        }

        return copy.deepcopy(response)

    def set_user(self):
        cua = CustomerUserApi(self.context)

        self.user["email"] = Tools.random_email() if self.options["email"] is None else self.options["email"]
        self.user["firstName"] = Tools.random_string_l()
        self.user["lastName"] = Tools.random_string_l()
        if self.options["group"] != "SUPER":
            pass
            #not implemented

        self.user_id = cua.create_customer_user(copy.deepcopy(self.user))
        if (self.user_id is not None):
            self.context.dynamic_context["delete_customer_user_id"].append(self.user_id)