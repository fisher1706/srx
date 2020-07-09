from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.resources.tools import Tools
from src.api.setups.setup_locker import setup_locker
import copy

def setup_smart_shelves(context, iothub=True, shipto=None, no_weight=False, distributor_id=None):
    if (shipto is not None):
        response_locker = setup_locker(context, shipto=shipto)
        locker_body = response_locker["locker"]
    else:
        response_locker = setup_locker(context)
        locker_body = response_locker["locker"]
    ssa = SmartShelvesApi(context)
    first_door_configuration = ssa.get_door_configuration(locker_body["id"])[0]
    smart_shelves_dto = Tools.get_dto("smart_shelves_dto.json")
    smart_shelves_dto["serialNumber"] = Tools.random_string_u()
    smart_shelves_dto["distributor"]["id"] = context.data.distributor_id
    smart_shelves_dto["doorConfiguration"]["id"] = first_door_configuration["id"]
    smart_shelves_dto["doorConfiguration"]["hardware"]["id"] = locker_body["id"]
    ssa.create_smart_shelf(smart_shelves_dto)
    smart_shelves_id = ssa.get_smart_shelves_id(locker_body["value"])
    context.dynamic_context["delete_smart_shelf_id"].append(smart_shelves_id)
    response = {
        "locker": locker_body,
        "iothub": response_locker["iothub"],
        "door": first_door_configuration,
        "smart_shelves_id": smart_shelves_id,
        "smart_shelf_number": smart_shelves_dto["serialNumber"]
    }

    return copy.deepcopy(response)