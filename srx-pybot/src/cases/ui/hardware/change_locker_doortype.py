from src.pages.sub.login_page import LoginPage
from src.pages.admin.hardware_page import HardwarePage
from src.api.admin.hardware_api import HardwareApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.locker_basis import locker_basis
import time

def change_locker_doortype(case):
    case.log_name("Change locker doortype (Weight/NoWeight)")
    case.testrail_config(1851)

    try:
        lp = LoginPage(case.activity)
        hp = HardwarePage(case.activity)
        ha = HardwareApi(case)

        response = locker_basis(case)
        locker_body = response["locker"]
        iothub_body = response["iothub"]

        lp.log_in_admin_portal()
        hp.sidebar_hardware()
        hp.check_last_hardware(serial_number=locker_body["value"], device_type="LOCKER", iothub=str(iothub_body["id"]), device_subtype=locker_body["lockerType"]["name"])
        doors_data = hp.configure_locker_door()
        hp.check_locker_door(doors_data)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    change_locker_doortype(Case(Activity()))