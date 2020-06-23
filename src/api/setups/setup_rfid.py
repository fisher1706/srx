from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.resources.tools import Tools
import copy

def setup_rfid(context, shipto=None):
    aha = AdminHardwareApi(context)

    rfid_body = aha.create_rfid()
    context.dynamic_context["delete_hardware_id"].append(rfid_body["id"])

    if (shipto is not None):
        ua = UserApi(context)
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
            "distributorId": context.data.distributor_id,
            "distributorName": context.data.distributor_name,
            "type": "RFID",
            "value": rfid_body["value"]
        }

        dha = DistributorHardwareApi(context)
        dha.update_hardware(rfid_dto)

    return copy.deepcopy(rfid_body)