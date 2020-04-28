from src.api.admin.hardware_api import HardwareApi as AdminHardwareApi
from src.api.distributor.user_api import UserApi
from src.api.distributor.hardware_api import HardwareApi as DistributorHardwareApi
from src.resources.tools import Tools
import copy
import time

def storage_basis(case, doorsQuantity, columnsQuantity, iothub=True, iothub_body=None, shipto=None, distributor_id=None):
    aha = AdminHardwareApi(case)
    if (distributor_id is None):
        if (iothub == True):
            iothub_body = aha.create_iothub()
            iothub_id = iothub_body["id"]
        elif (iothub == None):
            iothub_body = None
            iothub_id = None
        else:
            iothub_id = iothub

    elif (distributor_id is not None):
        if (iothub == True):
            iothub_body = aha.create_iothub(distributor_id)
            iothub_id = iothub_body["id"]
        elif (iothub == None):
            iothub_body = None
            iothub_id = None
        else:
            iothub_id = iothub

    time.sleep(5)
    storage_body = aha.create_storage(doorsQuantity, columnsQuantity, iothub_id=iothub_body["id"])

    response = {
        "iothub": iothub_body,
        "storage": storage_body
    }

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

        response = {
        "iothub": iothub_body,
        "storage": storage_body,
        "shipTo": shipto,
        "customerUser": customer_user["id"]
    }

    return copy.deepcopy(response)