import copy
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools

class SetupShiptoCustomer(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "ShipTo"
        self.options = {
            "subsite_id": None,
            "distributor_id": None,
            "number": None,
            "checkout_settings": None,
            "autosubmit_settings": None,
            "reorder_controls_settings": None,
            "delete": True,
            "expected_status_code": None,
        }
        self.shipto = Tools.get_dto("shipto_dto.json")
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
        sa = ShiptoApi(self.context)

        self.shipto["number"] = self.options["number"] if self.options["number"] is not None else Tools.random_string_l(10)
        self.shipto["address"] = {
            "zipCode": "12345",
            "line1": "addressLn1",
            "line2": "addressLn1",
            "city": "Ct",
            "state": "AL"
        }
        self.shipto["poNumber"] = Tools.random_string_l(10)
        self.shipto["apiWarehouse"] = {
            "id": self.context.data.warehouse_id
        }

        self.shipto_id = sa.create_shipto(copy.deepcopy(self.shipto), expected_status_code=self.options["expected_status_code"], customer_id=self.customer_id)
        if self.shipto_id is not None and self.options["delete"]:
            self.context.dynamic_context["delete_shipto_id"].append(self.shipto_id)

    def set_checkout_settings(self):
        pass

    def set_reorder_controls_settings(self):
        if self.options["reorder_controls_settings"] is not None:
            sta = SettingsApi(self.context)
            if self.options["reorder_controls_settings"] == "DEFAULT":
                sta.set_reorder_controls_settings_for_shipto(self.shipto_id)
            elif isinstance(self.options["reorder_controls_settings"], dict):
                sta.set_reorder_controls_settings_for_shipto(
                    self.shipto_id,
                    self.options["reorder_controls_settings"].get("reorder_controls"),
                    self.options["reorder_controls_settings"].get("track_ohi"),
                    self.options["reorder_controls_settings"].get("scan_to_order"),
                    self.options["reorder_controls_settings"].get("enable_reorder_control"))
            else:
                self.context.logger.warning(f"Unknown 'reorder_controls_settings' option: '{self.options['reorder_controls_settings']}'")

    def set_autosubmit_settings(self):
        pass
