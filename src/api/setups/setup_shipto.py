from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupShipto(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "ShipTo"
        self.options = {
            "checkout_settings": None,
            "autosubmit_settings": None,
            "serialization_settings": None
        }
        self.shipto = Tools.get_dto("shipto_dto.json")

    def setup(self):
        self.set_shipto()
        self.set_checkout_settings()
        self.set_autosubmit_settings()
        self.set_serialization_settings()

        response = {
            "shipto": self.shipto,
            "shipto_id": self.id
        }

        return copy.deepcopy(response)

    def set_shipto(self):
        sa = ShiptoApi(self.context)

        self.shipto["number"] = Tools.random_string_l(10)
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

        self.id = sa.create_shipto(copy.deepcopy(self.shipto))
        self.context.dynamic_context["delete_shipto_id"].append(self.id)

    def set_checkout_settings(self):
        if (self.options["checkout_settings"] is not None):
            sta = SettingsApi(self.context)
            if (self.options["checkout_settings"] == "DEFAULT"):
                sta.set_checkout_software_settings_for_shipto(self.id)
            elif (type(self.options["checkout_settings"]) is dict):
                sta.set_checkout_software_settings_for_shipto(
                    self.id, 
                    self.options["checkout_settings"].get("reorder_controls"),
                    self.options["checkout_settings"].get("track_ohi"),
                    self.options["checkout_settings"].get("scan_to_order"),
                    self.options["checkout_settings"].get("enable_reorder_control"))
            else:
                self.context.logger.warning(f"Unknown 'checkout_settings' option: '{self.options['checkout_settings']}'")

    def set_autosubmit_settings(self):
        if (self.options["autosubmit_settings"] is not None):
            sta = SettingsApi(self.context)
            if (self.options["autosubmit_settings"] == "DEFAULT"):
                sta.set_autosubmit_settings_shipto(self.id)
            elif (type(self.options["autosubmit_settings"]) is dict):
                sta.set_autosubmit_settings_shipto(
                    self.id,
                    self.options["autosubmit_settings"].get("enabled"),
                    self.options["autosubmit_settings"].get("immediately"),
                    self.options["autosubmit_settings"].get("as_order"))
            else:
                self.context.logger.warning(f"Unknown 'autosubmit_settings' option: '{self.options['autosubmit_settings']}'")

    def set_serialization_settings(self):
        if (self.options["serialization_settings"] is not None):
            sta = SettingsApi(self.context)
            if (self.options["serialization_settings"] == "OFF"):
                sta.set_serialization_settings_shipto(self.id)
            elif (type(self.options["serialization_settings"]) is dict):
                sta.set_serialization_settings_shipto(
                    self.id,
                    self.options["serialization_settings"].get("expiration"),
                    self.options["serialization_settings"].get("alarm"))
            else:
                self.context.logger.warning(f"Unknown 'serialization_settings' option: '{self.options['serialization_settings']}'")