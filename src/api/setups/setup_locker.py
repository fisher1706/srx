from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.api.setups.base_setup import BaseSetup
from src.resources.tools import Tools
import copy
import time

class SetupLocker(BaseSetup):
    def __init__(self, context):
        super().__init__(context)
        
        self.setup_name = "Locker"
        self.options = {
            "iothub": True,
            "shipto_id": None,
            "no_weight": None,
            "distributor_id": None,
            "smart_shelf": None
        }
        self.iothub = None
        self.locker = None
        self.smart_shelf_number = None
        self.iothub_id = None
        self.locker_id = None
        self.smart_shelf_id = None
        self.door = None

    def setup(self):
        self.set_hardware()
        self.set_shipto()
        self.set_smart_shelf()

        response = {
            "iothub": self.iothub,
            "iothub_id": self.iothub_id,
            "locker": self.locker,
            "locker_id": self.locker_id,
            "smart_shelf_number": self.smart_shelf_number,
            "smart_shelf_id": self.smart_shelf_id,
            "door": self.door
        }

        return copy.deepcopy(response)

    def set_hardware(self):
        aha = AdminHardwareApi(self.context)
        if (self.options["distributor_id"] is None):
            if (self.options["iothub"]):
                self.iothub = aha.create_iothub()
                self.iothub_id = self.iothub["id"]
        else:
            if (self.options["iothub"]):
                self.iothub = aha.create_iothub(self.options["distributor_id"])
                self.iothub_id = self.iothub["id"]
        self.context.dynamic_context["delete_hardware_id"].append(self.iothub_id)
        first_locker_type_id = (aha.get_first_locker_type())["id"]
        time.sleep(5)
        self.locker = aha.create_locker(locker_type_id=first_locker_type_id, iothub_id=self.iothub_id)
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

    def set_smart_shelf(self):
        if (self.options["smart_shelf"]):
            ssa = SmartShelvesApi(self.context)
            self.door = ssa.get_door_configuration(self.locker_id)[0]
            smart_shelves_dto = Tools.get_dto("smart_shelves_dto.json")
            smart_shelves_dto["serialNumber"] = Tools.random_string_u()
            smart_shelves_dto["distributor"]["id"] = self.data.distributor_id
            smart_shelves_dto["doorConfiguration"]["id"] = self.door["id"]
            smart_shelves_dto["doorConfiguration"]["hardware"]["id"] = self.locker_id
            ssa.create_smart_shelf(smart_shelves_dto)
            self.smart_shelf_id = ssa.get_smart_shelves_id(self.locker["value"])
            self.context.dynamic_context["delete_smart_shelf_id"].append(self.smart_shelf_id)
            self.smart_shelf_number = smart_shelves_dto["serialNumber"]