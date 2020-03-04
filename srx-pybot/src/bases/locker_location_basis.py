from src.bases.location_basis import location_basis
from src.bases.locker_basis import locker_basis
from src.api.distributor.user_api import UserApi
from src.api.distributor.hardware_api import HardwareApi as DistributorHardwareApi
from src.api.admin.hardware_api import HardwareApi as AdminHardwareApi
import copy

def locker_location_basis(case, no_weight=False):
        response = locker_basis(case)
        locker_body = response["locker"]
        iothub_body = response["iothub"]

        location_pairs = {
            "attributeName1": "Locker",
            "attributeValue1": locker_body["value"],
            "attributeName2": "Door",
            "attributeValue2": "1",
            "attributeName3": "Cell",
            "attributeValue3": "1",
            "attributeName4": None,
            "attributeValue4": None
        }

        if (no_weight == True):
            aha = AdminHardwareApi(case)
            aha.update_locker_configuration(locker_body["id"], 1, True)

        response = location_basis(case, location_pairs=location_pairs, location_type="LOCKER")
        product_body = response["product"]
        shipto_body = response["shipto"]
        location_body = response["location"]
        new_shipto = response["shipto_id"]

        ua = UserApi(case)
        customer_user = ua.get_first_customer_user(new_shipto)
        distributor_user = ua.get_first_distributor_user(new_shipto)

        iothub_dto = {}
        iothub_dto["id"] = iothub_body["id"]
        iothub_dto["customerUser"] = {
            "id": customer_user["id"]
        }
        iothub_dto["distributorUser"] = {
            "id": distributor_user["id"]
        }
        iothub_dto["deviceName"] = case.random_string_u()
        iothub_dto["shipToId"] = new_shipto
        iothub_dto["distributorId"] = case.activity.variables.distributor_id
        iothub_dto["distributorName"] = case.activity.variables.distributor_name
        iothub_dto["type"] = "IOTHUB"
        iothub_dto["value"] = iothub_body["value"]

        dha = DistributorHardwareApi(case)
        dha.update_hardware(iothub_dto)

        response = {
            "locker": locker_body,
            "iothub": iothub_body,
            "product": product_body,
            "shipto": shipto_body,
            "location": location_body,
            "shipto_id": new_shipto
        }

        return copy.deepcopy(response)