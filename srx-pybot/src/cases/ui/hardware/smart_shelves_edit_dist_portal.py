from src.pages.sub.login_page import LoginPage
from src.pages.distributor.distributor_portal_smart_shelves_page import DistributorSmartShelvesPage
from src.api.admin.hardware_api import HardwareApi
from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.locker_basis import locker_basis
from src.bases.smart_shelves_basis import smart_shelves_basis
import time

def smart_shelves_edit_dist_portal(case):
    case.log_name("Distributor portal: Edit Smart Shelves ")
    case.testrail_config(1960)

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

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body, locker_body_second=False)

        #--------------------------------
        smart_shelves_body = dss.smart_shelves_body.copy()
        smart_shelves_body["serialNumber"] = response["smart_shelf_number"]
        smart_shelves_body["assign_to"] = locker
        smart_shelves_body["door_number"] = "1"

        lp.log_in_distributor_portal()
        dss.open_smart_shelves()
        dss.update_smart_shelves(smart_shelves_body)
        dss.check_last_smart_shelf(smart_shelves_body)

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
    smart_shelves_edit_dist_portal(Case(Activity()))