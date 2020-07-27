from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy
import time

class LockerSetup(BaseSetup):
    setup_name = "Locker"
    options = {
        "iothub": None,
        "shipto_id": None,
        "no_weight": None,
        "distributor_id": None
    }
    iothub = None
    locker = None

    def setup(self):
        self.set_hardware()
        self.set_shipto()

        response = {
            "iothub": self.iothub,
            "iothub_id": self.iothub_id,
            "locker": self.locker,
            "locker_id": self.locker_id
        }

        return copy.deepcopy(response)

    def set_hardware(self):
        aha = AdminHardwareApi(self.context)
        if (self.options["distributor_id"] is None):
            if (self.options["iothub"]):
                self.iothub = aha.create_iothub()
                self.iothub_id = iothub["id"]
        else:
            if (self.options["iothub"]):
                self.iothub = aha.create_iothub(self.options["distributor_id"])
                self.iothub_id = iothub["id"]
        self.context.dynamic_context["delete_hardware_id"].append(self.iothub_id)
        first_locker_type_id = (aha.get_first_locker_type())["id"]
        time.sleep(5)
        self.locker = aha.create_locker(locker_type_id=first_locker_type_id, iothub_id=iothub_id)
        self.locker_id = self.locker["id"]
        self.context.dynamic_context["delete_hardware_id"].insert(0, self.locker_id)
        if (self.options["no_weight"]):
            aha.update_locker_configuration(self.locker_id, True)

    def set_shipto(self):
        if (self.options["shipto_id"] is not None):
            iothub_dto = {}
            iothub_dto["id"] = self.iothub_id
            iothub_dto["deviceName"] = Tools.random_string_u()
            iothub_dto["shipToId"] = self.options["shipto_id"]
            iothub_dto["distributorId"] = self.context.data.distributor_id
            iothub_dto["distributorName"] = self.context.data.distributor_name
            iothub_dto["type"] = "IOTHUB"
            iothub_dto["value"] = self.iothub["value"]

            dha = DistributorHardwareApi(self.context)
            dha.update_hardware(iothub_dto)