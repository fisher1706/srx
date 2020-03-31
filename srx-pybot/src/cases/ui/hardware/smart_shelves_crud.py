from src.pages.sub.login_page import LoginPage
from src.pages.admin.smart_shelves_page import SmartShelvesPage
from src.api.admin.hardware_api import HardwareApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.locker_basis import locker_basis
import time
import random

def smart_shelves_crud(case):
    case.log_name("Smart Shelves CRUD")
    case.testrail_config(case.activity.variables.run_number, 1920)

    try:
        lp = LoginPage(case.activity)
        sh = SmartShelvesPage(case.activity)
        ha = HardwareApi(case)

        # create locker for main distributor
        response = locker_basis(case)
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        # create locker for second distributor
        response_second = locker_basis(case, distributor_id=case.activity.variables.sub_distributor_id)
        locker_body_second = response_second["locker"]
        edit_locker = locker_body_second["value"]
        iothub_body_second = response_second["iothub"]

        #--------------------------------
        serial_number = random.randint(1000000, 9999999)
        smart_shelves_body = sh.smart_shelves_body.copy()
        smart_shelves_body["serialNumber"] = f"{serial_number}"
        smart_shelves_body["distributor"] = f"{case.activity.variables.distributor_name}"
        smart_shelves_body["assign_to"] = f"{locker}"
        smart_shelves_body["door_number"] = "1"

        #--------------------------------
        edit_serial_number = f"edit{serial_number}"
        edit_smart_shelves_body = sh.smart_shelves_body.copy()
        edit_smart_shelves_body["serialNumber"] = f"{edit_serial_number}"
        edit_smart_shelves_body["distributor"] = f"{case.activity.variables.sub_distributor_name}"
        edit_smart_shelves_body["assign_to"] = f"{edit_locker}"
        edit_smart_shelves_body["door_number"] = "2"

        lp.log_in_admin_portal()
        sh.open_smart_shelves()
        sh.create_smart_shelves(smart_shelves_body)
        sh.check_last_smart_shelf(smart_shelves_body)
        sh.update_smart_shelves(edit_smart_shelves_body)
        sh.check_last_smart_shelf(edit_smart_shelves_body)
        sh.delete_smart_shelf(edit_serial_number)
        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        ha.delete_hardware(locker_body_second["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        ha.delete_hardware(iothub_body_second["id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    smart_shelves_crud(Case(Activity()))