from src.api.distributor.user_api import UserApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupDistributorUser(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Distributor User"
        self.options = {
            "expected_status_code": None
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

        self.user["email"] = Tools.random_email()
        self.user["firstName"] = Tools.random_string_l()
        self.user["lastName"] = Tools.random_string_l()
        self.user["userGroup"] = {
            "id": self.context.data.default_security_group_id
        }
        self.user["warehouses"] = [{
            "id": self.context.data.warehouse_id
        }]

        self.user_id = ua.create_distributor_user(copy.deepcopy(self.user), expected_status_code=self.options["expected_status_code"])
        if (self.user_id is not None):
            self.context.dynamic_context["delete_distributor_user_id"].append(self.user_id)