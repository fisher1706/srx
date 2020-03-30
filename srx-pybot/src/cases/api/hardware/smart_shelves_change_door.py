from src.pages.sub.login_page import LoginPage
from src.pages.admin.smart_shelves_page import SmartShelves
from src.api.admin.hardware_api import HardwareApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.smart_shelves_basis import smart_shelves_basis
from src.bases.locker_basis import locker_basis
from src.api.admin.smart_shelves_api import SmartShelvesApi
import time
import random

def smart_shelves_change_door(case):
    case.log_name("Change Locker door in smart shelf")
    case.testrail_config(case.activity.variables.run_number, 1923)

    try:
        ssa = SmartShelvesApi(case)
        ha = HardwareApi(case)

        # create smart shelf for main distributor
        response = smart_shelves_basis(case)
        locker_body = response["locker"]
        locker_id = locker_body["id"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        # create second locker
        response_second = locker_basis(case)
        locker_body_second = response_second["locker"]
        locker_id_second = locker_body_second["id"]
        locker_second = locker_body_second["value"]
        iothub_body_second = response_second["iothub"]

        ssa.update_smart_shelf(locker_body, locker_body_second=locker_body_second)
        locker_1_conf = ha.get_locker_configuration(locker_id)
        locker_2_conf = ha.get_locker_configuration(locker_id_second)
        assert (locker_1_conf[0]["smartShelfHardware"] == None), f"First locker should not have smart shelf with ID {response['smart_shelves_id']}"
        assert (locker_2_conf[0]["smartShelfHardware"]["id"] == response["smart_shelves_id"]), f"Second locker should have smart shelf with ID {response['smart_shelves_id']}"
        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_id)
        ha.delete_hardware(locker_body_second["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        ha.delete_hardware(iothub_body_second["id"])
        ssa.delete_smart_shelves(response["smart_shelves_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    smart_shelves_change_door(Case(Activity(api_test=True)))