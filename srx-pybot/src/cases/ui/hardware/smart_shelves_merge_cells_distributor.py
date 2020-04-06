from src.pages.sub.login_page import LoginPage
from src.pages.distributor.distributor_portal_smart_shelves_page import DistributorSmartShelvesPage
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.api.admin.hardware_api import HardwareApi
from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.locker_basis import locker_basis
from src.bases.smart_shelves_basis import smart_shelves_basis
import time

def smart_shelves_merge_cells_distributor(case):
    case.log_name("Distributor portal: Smart Shelves Merge/Split cells")
    case.testrail_config(case.activity.variables.run_number, 1959)

    try:
        lp = LoginPage(case.activity)
        dss = DistributorSmartShelvesPage(case.activity)
        ha = HardwareApi(case)
        ssa = SmartShelvesApi(case)

        # create smart shelf for main distributor
        response = smart_shelves_basis(case)
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        lp.log_in_distributor_portal()
        dss.open_smart_shelves()
        dss.merge_cells(3)
        dss.check_cells_number(2)
        dss.split_cells(0)
        dss.check_cells_number(4)

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
    smart_shelves_merge_cells_distributor(Case(Activity()))