from src.api.admin.hardware_api import HardwareApi as AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.hardware_api import HardwareApi as DistributorHardwareApi
from src.resources.tools import Tools
import copy

def rfid_basis(case, shipto=None):
    aha = AdminHardwareApi(case)

    rfid_body = aha.create_rfid()

    if (shipto is not None):
        ua = UserApi(case)
        customer_user = ua.get_first_customer_user(shipto)
        distributor_user = ua.get_first_distributor_user(shipto)

        rfid_dto = {
            "id": rfid_body["id"],
            "customerUser": {
                "id": customer_user["id"]
            },
            "distributorUser": {
                "id": distributor_user["id"]
            },
            "deviceName": Tools.random_string_u(),
            "shipToId": shipto,
            "distributorId": case.activity.variables.distributor_id,
            "distributorName": case.activity.variables.distributor_name,
            "type": "RFID",
            "value": rfid_body["value"]
        }

        dha = DistributorHardwareApi(case)
        dha.update_hardware(rfid_dto)

    return copy.deepcopy(rfid_body)