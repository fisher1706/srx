from src.api.admin.hardware_api import HardwareApi
import copy
import time

def locker_basis(case, iothub=True):
    ha = HardwareApi(case)
    if (iothub == True):
        iothub_dto = ha.create_iothub()
        iothub_id = iothub_dto["id"]
    else:
        iothub_dto = None
        iothub_id = None
    first_locker_type_id = (ha.get_first_locker_type())["id"]
    time.sleep(5)
    locker_dto = ha.create_locker(locker_type_id=first_locker_type_id, iothub_id=iothub_id)

    response = {
        "iothub": iothub_dto,
        "locker": locker_dto
    }

    return copy.deepcopy(response)