from src.api.distributor.location_api import LocationApi
from src.api.setups.setup_shipto import SetupShipto
from src.api.setups.setup_product import SetupProduct
from src.api.setups.base_setup import BaseSetup
from src.api.distributor.shipto_api import ShiptoApi
from src.resources.tools import Tools
import copy

class SetupLocation(BaseSetup):
    setup_name = "Location"
    options = {
        "product": None,
        "shipto_id": None,
        "location_pairs": None,
        "type": "LABEL",
        "serialized": None,
        "lot": None,
        "autosubmit": None,
        "ohi": None
    }
    location = Tools.get_dto("location_dto.json")

    def __init__(self, context):
        super().__init__(context)
        self.setup_product = SetupProduct(self.context)
        self.setup_shipto = SetupShipto(self.context)

    def setup(self):
        self.set_shipto()
        self.set_product()
        self.set_location()

        response = {
            "product": self.product,
            "shipto": self.shipto,
            "location": self.location,
            "shipto_id": self.shipto_id
        }

        return copy.deepcopy(response)

    def set_shipto(self):
        if (self.options["shipto_id"] is None):
            self.shipto = self.setup_shipto.setup()
            self.shipto_id = self.shipto["shipto_id"]
        else:
            sha = ShiptoApi(self.context)
            self.shipto_id = self.options["shipto_id"]
            self.shipto = sha.get_shipto_by_id(self.shipto_id)

    def set_product(self):
        if (self.options["product"] is None):
            self.product = self.setup_product.setup()
        else:
            self.product = self.options["product"]

    def set_location(self):
        la = LocationApi(self.context)

        if (self.options["location_pairs"] is None):
            self.location["attributeName1"] = self.product["partSku"]
            self.location["attributeValue1"] = self.product["partSku"]
        else:
            self.location["attributeName1"] = self.options["location_pairs"]["attributeName1"]
            self.location["attributeValue1"] = self.options["location_pairs"]["attributeValue1"]
            self.location["attributeName2"] = self.options["location_pairs"]["attributeName2"]
            self.location["attributeValue2"] = self.options["location_pairs"]["attributeValue2"]
            self.location["attributeName3"] = self.options["location_pairs"]["attributeName3"]
            self.location["attributeValue3"] = self.options["location_pairs"]["attributeValue3"]
            self.location["attributeName4"] = self.options["location_pairs"]["attributeName4"]
            self.location["attributeValue4"] = self.options["location_pairs"]["attributeValue4"]

        self.location["orderingConfig"] = {
            "product": {
                "partSku": self.product["partSku"]
            },
            "type": self.options["type"],
            "currentInventoryControls": {
                "min": self.product["roundBuy"],
                "max": self.product["roundBuy"]*3
            }
        }
        self.location["onHandInventory"] = self.options["ohi"]
        self.location["serialized"] = bool(self.options["serialized"])
        self.location["lot"] = bool(self.options["lot"])
        if (self.options["autosubmit"] is not None):
            self.location["autoSubmit"] = bool(self.options["autosubmit"])
        
        location_list = [copy.deepcopy(self.location)]
        la.create_location(copy.deepcopy(location_list), self.shipto_id)