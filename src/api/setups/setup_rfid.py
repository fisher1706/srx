from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy

class SetupRfid(BaseSetup):
    setup_name = "RFID"
    options = {
        "shipto_id": None
    }
    rfid = None

    def setup(self):
        self.set_rfid()
        self.set_shipto()

        return copy.deepcopy(self.rfid)

    def set_rfid(self):
        aha = AdminHardwareApi(self.context)

        self.rfid = aha.create_rfid()
        self.context.dynamic_context["delete_hardware_id"].append(self.rfid["id"])

    def set_shipto(self):
        if (self.options["shipto_id"] is not None):
            rfid_dto = {
                "id": self.rfid["id"],
                "deviceName": Tools.random_string_u(),
                "shipToId": self.options["shipto_id"],
                "distributorId": self.context.data.distributor_id,
                "distributorName": self.context.data.distributor_name,
                "type": "RFID",
                "value": self.rfid["value"]
            }

            dha = DistributorHardwareApi(self.context)
            dha.update_hardware(rfid_dto)