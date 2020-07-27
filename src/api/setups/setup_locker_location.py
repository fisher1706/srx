from src.api.setups.setup_location import setup_location
from src.api.setups.setup_locker import setup_locker
from src.api.distributor.user_api import UserApi
from src.api.distributor.distributor_hardware_api import DistributorHardwareApi
from src.api.admin.admin_hardware_api import AdminHardwareApi
from src.resources.tools import Tools
import copy

def setup_locker_location(context, no_weight=False, is_asset=None):
        response_locker = setup_locker(context)
        locker_body = response_locker["locker"]
        iothub_body = response_locker["iothub"]

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
            aha = AdminHardwareApi(context)
            aha.update_locker_configuration(locker_body["id"], True)

        response_location = setup_location(context, location_pairs=location_pairs, location_type="LOCKER", is_asset=is_asset)
        product_body = response_location["product"]
        shipto_body = response_location["shipto"]
        location_body = response_location["location"]
        new_shipto = response_location["shipto_id"]

        ua = UserApi(context)
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
        iothub_dto["deviceName"] = Tools.random_string_u()
        iothub_dto["shipToId"] = new_shipto
        iothub_dto["distributorId"] = context.data.distributor_id
        iothub_dto["distributorName"] = context.data.distributor_name
        iothub_dto["type"] = "IOTHUB"
        iothub_dto["value"] = iothub_body["value"]

        dha = DistributorHardwareApi(context)
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