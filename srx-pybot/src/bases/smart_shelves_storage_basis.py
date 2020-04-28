from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.resources.tools import Tools
from src.bases.locker_basis import locker_basis

import copy
import time

def smart_shelves_storage_basis(case, no_weight=False, distributor_id=None, storage_body=None, door_number=None):
    ssa = SmartShelvesApi(case)

    if (storage_body is not None):
        storage_id = storage_body["id"]

    if (door_number is not None):
        door_configuration = ssa.get_storage_door_configuration(storage_id)[door_number]
    else:
        door_configuration = ssa.get_storage_door_configuration(storage_id)[0]

    smart_shelves_dto = Tools.get_dto("smart_shelves_dto.json")
    smart_shelves_dto["serialNumber"] = Tools.random_string_u()
    smart_shelves_dto["distributor"]["id"] = case.activity.variables.distributor_id
    smart_shelves_dto["doorConfiguration"]["id"] = door_configuration["id"]
    smart_shelves_dto["doorConfiguration"]["hardware"]["id"] = storage_id
    ssa.create_smart_shelf(smart_shelves_dto)
    smart_shelves_id = ssa.get_smart_shelves_id(storage_body["value"])
    response = {
        "storage": storage_body,
        #"iothub": locker_response["iothub"],
        "door": door_configuration,
        "smart_shelves_id": smart_shelves_id,
        "smart_shelf_number": smart_shelves_dto["serialNumber"]
    }
    return copy.deepcopy(response)