from src.api.admin.hardware_api import HardwareApi as AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.hardware_api import HardwareApi as DistributorHardwareApi
from src.resources.tools import Tools
import copy
import time

def locker_basis(case, iothub=True, shipto=None, no_weight=False, distributor_id=None):
    aha = AdminHardwareApi(case)
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

    first_locker_type_id = (aha.get_first_locker_type())["id"]
    time.sleep(5)
    locker_body = aha.create_locker(locker_type_id=first_locker_type_id, iothub_id=iothub_id)

    response = {
        "iothub": iothub_body,
        "locker": locker_body
    }

    if (no_weight == True):
        aha.update_locker_configuration(locker_body["id"], True)

    if (shipto is not None):
        ua = UserApi(case)
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
        iothub_dto["distributorId"] = case.activity.variables.distributor_id
        iothub_dto["distributorName"] = case.activity.variables.distributor_name
        iothub_dto["type"] = "IOTHUB"
        iothub_dto["value"] = iothub_body["value"]

        dha = DistributorHardwareApi(case)
        dha.update_hardware(iothub_dto)

    return copy.deepcopy(response)