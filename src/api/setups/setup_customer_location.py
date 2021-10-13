import copy
from src.api.distributor.settings_api import SettingsApi
from src.api.distributor.location_api import LocationApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_organization import SetupOrganization
from src.api.setups.setup_customer_product import SetupCustomerProduct
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools

class SetupCustomerLocation(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        self.setup_name = "Location"
        self.options = {
            "product": None,
            "subsite_id": None,
            "supplier_id": None,
            "type": "LABEL",
            "autosubmit": None,
            "ohi": None,
            "transaction": None,
            "dsn": None,
            "min": None,
            "max": None,
            "critical_min": None
        }
        self.location = Tools.get_dto("customer_location_dto.json")
        self.location_id = None
        self.product = None
        self.organization = None
        self.transaction = {}
        self.setup_customer_product = SetupCustomerProduct(self.context)
        self.setup_organization = SetupOrganization(self.context)

    def setup(self):
        self.set_organization()
        self.set_product()
        self.set_location()
        self.set_transaction()

        response = {
            "product": self.product,
            "organization": self.organization,
            "location": self.location,
            "location_id": self.location_id,
            "transaction": self.transaction
        }

        return copy.deepcopy(response)

    def set_organization(self):
        if self.options["subsite_id"] is None or self.options["supplier_id"] is None:
            self.organization = self.setup_organization.setup()

            self.location["orderingConfig"]["product"]["distributor"]["id"] = self.organization["supplier_id"]
            self.location["sharedSpaceId"] = self.organization["subsite_id"]
            self.location["distributorId"] = self.organization["supplier_id"]
        else:
            self.location["orderingConfig"]["product"]["distributor"]["id"] = self.options["supplier_id"]
            self.location["sharedSpaceId"] = self.options["subsite_id"]
            self.location["distributorId"] = self.options["supplier_id"]

    def set_product(self):
        if self.options["product"] is None:
            self.product = self.setup_customer_product.setup()
        else:
            self.product = self.options["product"]

    def set_location(self):
        la = LocationApi(self.context)

        location_min = self.product["roundBuy"] if self.options["min"] is None else self.options["min"]
        location_max = self.product["roundBuy"]*3 if self.options["max"] is None else self.options["max"]
        self.location["orderingConfig"] = {
            "product": {
                "partSku": self.product["partSku"],
                "customerSku": self.product["customerSku"]
            },
            "type": self.options["type"],
            "currentInventoryControls": {
                "min": location_min,
                "max": location_max
            },
            "criticalMin": self.options["critical_min"] if self.options["critical_min"] is not None else None,
        }
        if self.options["ohi"] == "MAX":
            self.location["onHandInventory"] = location_max*self.product["packageConversion"]
        else:
            self.location["onHandInventory"] = self.options["ohi"]
        if self.options["autosubmit"] is not None:
            self.location["autoSubmit"] = bool(self.options["autosubmit"])
        la.create_location(copy.deepcopy(self.location))

    def set_transaction(self):
        pass
