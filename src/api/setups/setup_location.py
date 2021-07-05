from src.api.distributor.location_api import LocationApi
from src.api.distributor.shipto_api import ShiptoApi
from src.api.distributor.rfid_api import RfidApi
from src.api.distributor.transaction_api import TransactionApi
from src.api.setups.setup_shipto import SetupShipto
from src.api.setups.setup_product import SetupProduct
from src.api.setups.setup_locker import SetupLocker
from src.api.setups.setup_rfid import SetupRfid
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupLocation(BaseSetup):
    def __init__(self, context):
        super().__init__(context)

        self.setup_name = "Location"
        self.options = {
            "product": None,
            "shipto_id": None,
            "location_pairs": None,
            "type": "LABEL",
            "serialized": None,
            "lot": None,
            "autosubmit": None,
            "ohi": None,
            "locker_location": None,
            "rfid_location": None,
            "rfid_labels": None,
            "transaction": None,
            "dsn": None,
            "min": None,
            "max": None
        }
        self.location = Tools.get_dto("location_dto.json")
        self.location_id = None
        self.product = None
        self.shipto = None
        self.shipto_id = None
        self.customer_id = None
        self.iothub = None
        self.locker = None
        self.rfid = None
        self.transaction = {}
        self.put_away = {}
        self.rfid_labels = []
        self.setup_product = SetupProduct(self.context)
        self.setup_shipto = SetupShipto(self.context)
        self.setup_locker = SetupLocker(self.context)
        self.setup_rfid = SetupRfid(self.context)

    def setup(self, expected_status_code=None):
        self.expected_status_code = expected_status_code
        self.set_shipto()
        self.set_locker()
        self.set_rfid()
        self.set_product()
        self.set_location()
        self.set_rfid_labels()
        self.set_transaction()

        response = {
            "product": self.product,
            "shipto": self.shipto,
            "location": self.location,
            "location_id": self.location_id,
            "shipto_id": self.shipto_id,
            "customer_id": self.customer_id,
            "iothub": self.iothub,
            "locker": self.locker,
            "rfid": self.rfid,
            "rfid_labels": self.rfid_labels,
            "transaction": self.transaction,
            "put_away": self.put_away,
        }

        return copy.deepcopy(response)

    def set_locker(self):
        if (self.options["locker_location"]):
            self.setup_locker.add_option("shipto_id", self.shipto_id)
            response_locker = self.setup_locker.setup()
            self.locker = response_locker["locker"]
            self.iothub = response_locker["iothub"]
            self.options["type"] = "LOCKER"

    def set_rfid(self):
        if (self.options["rfid_location"]):
            self.setup_rfid.add_option("shipto_id", self.shipto_id)
            self.rfid = self.setup_rfid.setup()
            self.options["type"] = "RFID"

    def set_shipto(self):
        if (self.options["shipto_id"] is None):
            shipto_response = self.setup_shipto.setup()
            self.shipto = shipto_response["shipto"]
            self.shipto_id = shipto_response["shipto_id"]
            self.customer_id = shipto_response["customer_id"]
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

        if (self.options["locker_location"]):
            self.location["attributeName1"] = "Locker"
            self.location["attributeValue1"] = self.locker["value"]
            self.location["attributeName2"] = "Door"
            self.location["attributeValue2"] = "1"
            self.location["attributeName3"] = "Cell"
            self.location["attributeValue3"] = "1"
        elif (self.options["location_pairs"] is None):
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

        location_min = self.product["roundBuy"] if self.options["min"] is None else self.options["min"]
        location_max = self.product["roundBuy"]*3 if self.options["max"] is None else self.options["max"]
        self.location["orderingConfig"] = {
            "product": {
                "partSku": self.product["partSku"]
            },
            "type": self.options["type"],
            "currentInventoryControls": {
                "min": location_min,
                "max": location_max
            },
            "dsn": self.options["dsn"]
        }
        if (self.options["ohi"] == "MAX"):
            self.location["onHandInventory"] = location_max*self.product["packageConversion"]
        else:
            self.location["onHandInventory"] = self.options["ohi"]
            self.location["serialized"] = bool(self.options["serialized"])
            self.location["lot"] = bool(self.options["lot"])
        if (self.options["autosubmit"] is not None):
            self.location["autoSubmit"] = bool(self.options["autosubmit"])
        
        location_list = [copy.deepcopy(self.location)]
        la.create_location(copy.deepcopy(location_list), self.shipto_id, expected_status_code=self.expected_status_code, customer_id=self.customer_id)
        if (self.expected_status_code is None):
            self.location_id = la.get_location_by_sku(self.shipto_id, self.product["partSku"], customer_id=self.customer_id)[-1]["id"]

    def set_rfid_labels(self):
        if (self.options["rfid_labels"] is not None):
            ra = RfidApi(self.context)
            la = LocationApi(self.context)
            location_id = la.get_location_by_sku(self.shipto_id, self.product["partSku"])[-1]["id"]
            for index in range(self.options["rfid_labels"]):
                self.rfid_labels.append(ra.create_rfid(location_id))

    def set_transaction(self):
        ta = TransactionApi(self.context)
        la = LocationApi(self.context)

        if (self.options["transaction"] is not None):
            if (self.options["type"] == "LABEL" or self.options["type"] == "BUTTON"):
                ordering_config_id = la.get_ordering_config_by_sku(self.shipto_id, self.product["partSku"])
                ta.create_active_item(self.shipto_id, ordering_config_id, repeat=6)
                transaction = ta.get_transaction(sku=self.product["partSku"], shipto_id=self.shipto_id)
                transaction_id = transaction["entities"][0]["id"]
                reorderQuantity = transaction["entities"][0]["reorderQuantity"]

                if (self.options["transaction"] != "ACTIVE"):
                    ta.update_replenishment_item(transaction_id, reorderQuantity, self.options["transaction"])

                self.transaction = {
                    "transaction_id": transaction_id,
                    "reorderQuantity": reorderQuantity
                }

                self.put_away = {
                    "shipToId": self.shipto_id,
                    "partSku": self.product["partSku"],
                    "quantity": reorderQuantity,
                    "transactionId": transaction_id
                }