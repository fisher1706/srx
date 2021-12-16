import copy
from src.api.customer.organization_api import OrganizationApi
from src.api.customer.customer_settings_api import CustomerSettingsApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools

class SetupCustomerShipto(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "ShipTo"
        self.options = {
            "subsite_id": None,
            "supplier_id": None,
            "number": None,
            "checkout_settings": None,
            "autosubmit_settings": None,
            "reorder_controls_settings": None,
            "expected_status_code": None,
        }
        self.shipto = Tools.get_dto("customer_shipto_dto.json")
        self.shipto_id = None

    def setup(self):
        self.set_shipto()
        self.set_checkout_settings()
        self.set_autosubmit_settings()
        self.set_reorder_controls_settings()

        response = {
            "shipto": self.shipto,
            "shipto_id": self.shipto_id,
        }

        return copy.deepcopy(response)

    def set_shipto(self):
        oa = OrganizationApi(self.context)

        self.shipto["number"] = self.options["number"] if self.options["number"] is not None else Tools.random_string_l(10)
        self.shipto["name"] = Tools.random_string_l(10)
        self.shipto["poNumber"] = Tools.random_string_l(10)
        self.shipto["distributorId"] = self.options["supplier_id"]
        self.shipto["sharedSpaceId"] = self.options["subsite_id"]

        self.shipto_id = oa.create_shipto(copy.deepcopy(self.shipto))
        if self.shipto_id is not None:
            #adding to both ID lists to be able to delete shiptos from different portal
            shipto = {
                    "shipto_id": self.shipto_id,
                    "customer_id": None
                }
            self.context.dynamic_context["delete_shipto_id"].append(shipto)
            self.context.dynamic_context["delete_customer_shipto_id"].append(self.shipto_id)

    def set_checkout_settings(self):
        pass

    def set_reorder_controls_settings(self):
        if self.options["reorder_controls_settings"] is not None:
            sta = CustomerSettingsApi(self.context)
            if self.options["reorder_controls_settings"] == "DEFAULT":
                sta.set_reorder_controls_settings_for_shipto(self.options["supplier_id"])
            elif isinstance(self.options["reorder_controls_settings"], dict):
                sta.set_reorder_controls_settings_for_shipto(
                    self.options["supplier_id"],
                    self.options["reorder_controls_settings"].get("reorder_controls"),
                    self.options["reorder_controls_settings"].get("track_ohi"),
                    self.options["reorder_controls_settings"].get("scan_to_order"),
                    self.options["reorder_controls_settings"].get("enable_reorder_control"))
            else:
                self.context.logger.warning(f"Unknown 'reorder_controls_settings' option: '{self.options['reorder_controls_settings']}'")

    def set_autosubmit_settings(self):
        pass
