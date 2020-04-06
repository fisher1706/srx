from src.pages.sub.login_page import LoginPage
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.api.admin.hardware_api import HardwareApi
from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.api.distributor.shipto_api import ShiptoApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.locker_basis import locker_basis
from src.bases.smart_shelves_basis import smart_shelves_basis
from src.bases.shipto_basis import shipto_basis
import time

def planogram_assign_smart_shelf(case):
    case.log_name("Assign smart shelf to locker via planogram")
    case.testrail_config(case.activity.variables.run_number, 1965)

    try:
        lp = LoginPage(case.activity)
        lpp = LockerPlanogramPage(case.activity)
        ha = HardwareApi(case)
        ssa = SmartShelvesApi(case)
        sta = ShiptoApi(case)

        #create shipto
        response_shipto = shipto_basis(case)

        # create smart shelf for main distributor
        response = smart_shelves_basis(case, shipto=response_shipto["shipto_id"])
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body, locker_body_second=False)

        lp.log_in_distributor_portal()
        lpp.follow_locker_planogram_url(customer_id=locker_body["customerUser"] , shipto_id=response_shipto["shipto_id"])
        lpp.assign_smart_shelf_to_locker_door(response["smart_shelf_number"])
        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        ssa.delete_smart_shelves(response["smart_shelves_id"])
        sta.delete_shipto(response_shipto["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    planogram_assign_smart_shelf(Case(Activity()))