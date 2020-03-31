from src.pages.sub.login_page import LoginPage
from src.pages.admin.smart_shelves_page import SmartShelvesPage
from src.pages.admin.hardware_page import HardwarePage
from src.api.admin.hardware_api import HardwareApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.smart_shelves_basis import smart_shelves_basis
from src.bases.locker_basis import locker_basis
from src.api.admin.smart_shelves_api import SmartShelvesApi
import time
import random

def smart_shelves_assign_to_several_lockers(case):
    case.log_name("Smart Shelves: Can not assign smart shelf to the locker door if smart shelf is already assigned to another locker(SRX-7951)")
    case.testrail_config(case.activity.variables.run_number, 1926)

    try:
        lp = LoginPage(case.activity)
        ss = SmartShelvesPage(case.activity)
        hp = HardwarePage(case.activity)
        ssa = SmartShelvesApi(case)
        ha = HardwareApi(case)

        # create smart shelf for main distributor
        response = smart_shelves_basis(case)
        smart_shelf_number = response["smart_shelf_number"]
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body, locker_body_second=False)

        # create second locker
        response_second = locker_basis(case)
        locker_body_second = response_second["locker"]
        locker_second = locker_body_second["value"]
        iothub_body_second = response_second["iothub"]

        lp.log_in_admin_portal()
        hp.sidebar_hardware()
        ss.assign_smart_shelf_locker_planogram(locker, smart_shelf_number)
        hp.sidebar_hardware()
        ss.check_smart_shelf_unavailable_via_planogram(locker, smart_shelf_number)
        
        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        ha.delete_hardware(locker_body_second["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        ha.delete_hardware(iothub_body_second["id"])
        ssa.delete_smart_shelves(response["smart_shelves_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    smart_shelves_assign_to_several_lockers(Case(Activity()))