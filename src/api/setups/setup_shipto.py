import copy
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.settings_api import SettingsApi
from src.api.setups.base_setup import BaseSetup
from src.api.setups.setup_customer import SetupCustomer
from src.resources.tools import Tools

class SetupShipto(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "ShipTo"
        self.options = {
            "number": None,
            "checkout_settings": None,
            "autosubmit_settings": None,
            "serialization_settings": None,
            "reorder_controls_settings": None,
            "delete": True,
            "customer": False,
            "expected_status_code": None,
            "customer.clc": None, #update current customer's settings
        }
        self.shipto = Tools.get_dto("shipto_dto.json")
        self.shipto_id = None
        self.customer_id = None
        self.setup_customer = SetupCustomer(self.context)

    def setup(self):
        self.set_customer()
        self.set_shipto()
        self.set_checkout_settings()
        self.set_autosubmit_settings()
        self.set_serialization_settings()
        self.set_reorder_controls_settings()
        self.set_customer_clc_settings()

        response = {
            "shipto": self.shipto,
            "shipto_id": self.shipto_id,
            "customer_id": self.customer_id
        }

        return copy.deepcopy(response)

    def set_customer(self):
        if self.options["customer"]:
            self.customer_id = self.setup_customer.setup()["customer_id"]

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
        if self.options["checkout_settings"] is not None:
            sta = SettingsApi(self.context)
            if self.options["checkout_settings"] == "DEFAULT":
                sta.set_checkout_settings(self.shipto_id)
            elif isinstance(self.options["checkout_settings"], dict):
                sta.set_checkout_settings(
                    self.shipto_id,
                    self.options["checkout_settings"].get("checkout_software"),
                    self.options["checkout_settings"].get("qr_code_kit"))
            else:
                self.context.logger.warning(f"Unknown 'checkout_settings' option: '{self.options['checkout_settings']}'")

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
        sta = SettingsApi(self.context)
        if self.options["autosubmit_settings"] is not None:
            if self.options["autosubmit_settings"] == "DEFAULT":
                sta.set_autosubmit_settings_shipto(self.shipto_id)
            elif isinstance(self.options["autosubmit_settings"], dict):
                sta.set_autosubmit_settings_shipto(
                    self.shipto_id,
                    self.options["autosubmit_settings"].get("enabled"),
                    self.options["autosubmit_settings"].get("immediately"),
                    self.options["autosubmit_settings"].get("as_order"))
            else:
                self.context.logger.warning(f"Unknown 'autosubmit_settings' option: '{self.options['autosubmit_settings']}'")
        else:
            sta.set_autosubmit_settings_shipto(self.shipto_id, False, False, False)

    def set_serialization_settings(self):
        if self.options["serialization_settings"] is not None:
            sta = SettingsApi(self.context)
            if self.options["serialization_settings"] == "OFF":
                sta.set_serialization_settings_shipto(self.shipto_id)
            elif isinstance(self.options["serialization_settings"], dict):
                sta.set_serialization_settings_shipto(
                    self.shipto_id,
                    self.options["serialization_settings"].get("expiration"),
                    self.options["serialization_settings"].get("alarm"))
            else:
                self.context.logger.warning(f"Unknown 'serialization_settings' option: '{self.options['serialization_settings']}'")

    def set_customer_clc_settings(self):
        if self.options["customer.clc"] is not None:
            sa = SettingsApi(self.context)
            sa.set_customer_level_catalog_flag(self.options["customer.clc"], self.customer_id)
