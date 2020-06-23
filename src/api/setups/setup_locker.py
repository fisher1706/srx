from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.resources.tools import Tools
import copy
import time

def setup_locker(context, iothub=True, shipto=None, no_weight=False, distributor_id=None):
    aha = AdminHardwareApi(context)
    if (distributor_id is None):
        if (iothub == True):
            iothub_body = aha.create_iothub()
            iothub_id = iothub_body["id"]
        else:
            iothub_body = None
            iothub_id = None
    elif (distributor_id is not None):
        if (iothub == True):
            iothub_body = aha.create_iothub(distributor_id)
            iothub_id = iothub_body["id"]
        else:
            iothub_body = None
            iothub_id = None
    context.dynamic_context["delete_hardware_id"].append(iothub_body["id"])
    first_locker_type_id = (aha.get_first_locker_type())["id"]
    time.sleep(5)
    locker_body = aha.create_locker(locker_type_id=first_locker_type_id, iothub_id=iothub_id)
    context.dynamic_context["delete_hardware_id"].insert(0, locker_body["id"]) 

    response = {
        "iothub": iothub_body,
        "locker": locker_body
    }

    if (no_weight == True):
        aha.update_locker_configuration(locker_body["id"], True)

    if (shipto is not None):
        ua = UserApi(context)
        customer_user = ua.get_first_customer_user(shipto)
        distributor_user = ua.get_first_distributor_user(shipto)

        iothub_dto = {}
        iothub_dto["id"] = iothub_body["id"]
        iothub_dto["customerUser"] = {
            "id": customer_user["id"]
        }
        iothub_dto["distributorUser"] = {
            "id": distributor_user["id"]
        }
        iothub_dto["deviceName"] = Tools.random_string_u()
        iothub_dto["shipToId"] = shipto
        iothub_dto["distributorId"] = context.data.distributor_id
        iothub_dto["distributorName"] = context.data.distributor_name
        iothub_dto["type"] = "IOTHUB"
        iothub_dto["value"] = iothub_body["value"]

        dha = DistributorHardwareApi(context)
        dha.update_hardware(iothub_dto)

        response = {
            "iothub": iothub_body,
            "locker": locker_body,
            "shipTo": shipto,
            "customerUser": customer_user["id"]
        }

    return copy.deepcopy(response)