from src.api.distributor.user_api import UserApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupDistributorUser(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Distributor User"
        self.options = {
            "expected_status_code": None,
            "email": None,
            "group": None
        }
        self.user = Tools.get_dto("distributor_user_dto.json")
        self.user_id = None

    def setup(self):
        self.set_user()

        response = {
            "user": self.user,
            "user_id": self.user_id
        }

        return copy.deepcopy(response)

    def set_user(self):
        ua = UserApi(self.context)

        self.user["email"] = Tools.random_email() if self.options["email"] is None else self.options["email"]
        self.user["firstName"] = Tools.random_string_l()
        self.user["lastName"] = Tools.random_string_l()
        if self.options["group"] != "SUPER":
            if self.options["group"] is None:
                self.user["userGroup"] = {
                    "id": self.context.data.default_security_group_id
                }
            else:
                self.user["userGroup"] = {
                    "id": self.options["group"]
                }
            self.user["warehouses"] = [{
                    "id": self.context.data.warehouse_id
            }]

        else:
            current_user = ua.get_current_user()
            self.user["userGroup"] = {
                "id": current_user["userGroup"]["id"]
            }
            self.user["warehouses"] = []

        self.user_id = ua.create_distributor_user(copy.deepcopy(self.user), expected_status_code=self.options["expected_status_code"])
        if (self.user_id is not None):
            self.context.dynamic_context["delete_distributor_user_id"].append(self.user_id)