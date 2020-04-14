from src.pages.sub.login_page import LoginPage
from src.api.admin.hardware_api import HardwareApi
from src.api.distributor.shipto_api import ShiptoApi
from src.pages.distributor.locker_planogram_page import LockerPlanogramPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.locker_basis import locker_basis
from src.bases.shipto_basis import shipto_basis
import time

def locker_planogram(case):
    case.log_name("Open locker planogram via hardware tab")
    case.testrail_config(1961)

    try:
        lp = LoginPage(case.activity)
        ha = HardwareApi(case)
        lpp = LockerPlanogramPage(case.activity)
        sta = ShiptoApi(case)

        #create shipto
        response_shipto = shipto_basis(case)

        # create locker with shipto
        response = locker_basis(case, shipto=response_shipto["shipto_id"])
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        lp.log_in_distributor_portal()
        lpp.sidebar_hardware()
        lpp.open_locker_planogram(locker, response_shipto["shipto_id"])
        

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        sta.delete_shipto(response_shipto["shipto_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    locker_planogram(Case(Activity()))