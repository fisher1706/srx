from src.pages.sub.login_page import LoginPage
from src.pages.admin.smart_shelves_page import SmartShelves
from src.api.admin.hardware_api import HardwareApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.smart_shelves_basis import smart_shelves_basis
from src.api.admin.smart_shelves_api import SmartShelvesApi
import time
import random

def smart_shelves_merge_cells(case):
    case.log_name("Smart Shelves Merge/Split cells")
    case.testrail_config(case.activity.variables.run_number, 1921)

    try:
        lp = LoginPage(case.activity)
        ss = SmartShelves(case.activity)
        ssa = SmartShelvesApi(case)
        ha = HardwareApi(case)

        # # create locker for main distributor
        response = smart_shelves_basis(case)
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        lp.log_in_admin_portal()
        ss.open_smart_shelves()
        ss.merge_cells(3)
        ss.check_cells_number(2)
        ss.split_cells(0)
        ss.check_cells_number(4)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        ssa.delete_smart_shelves(response["smart_shelves_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    smart_shelves_merge_cells(Case(Activity()))