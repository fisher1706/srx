from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.resources.tools import Tools
from src.bases.locker_basis import locker_basis

import copy
import time

def smart_shelves_basis(case, iothub=True, shipto=None, no_weight=False, distributor_id=None):
    locker_response = locker_basis(case)
    locker_body = locker_response["locker"]
    ssa = SmartShelvesApi(case)
    first_door_configuration = ssa.get_door_configuration(locker_body["id"])[0]
    smart_shelves_dto = Tools.get_dto("smart_shelves_dto.json")
    smart_shelves_dto["serialNumber"] = Tools.random_string_u()
    smart_shelves_dto["distributor"]["id"] = case.activity.variables.distributor_id
    smart_shelves_dto["doorConfiguration"]["id"] = first_door_configuration["id"]
    smart_shelves_dto["doorConfiguration"]["hardware"]["id"] = locker_body["id"]
    ssa.create_smart_shelf(smart_shelves_dto)
    smart_shelves_id = ssa.get_smart_shelves_id(locker_body["value"])
    response = {
        "locker": locker_body,
        "iothub": locker_response["iothub"],
        "door": first_door_configuration,
        "smart_shelves_id": smart_shelves_id
    }
    return copy.deepcopy(response)