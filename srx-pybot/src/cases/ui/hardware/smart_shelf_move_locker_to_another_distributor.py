from src.pages.sub.login_page import LoginPage
from src.pages.admin.smart_shelves_page import SmartShelvesPage
from src.api.admin.hardware_api import HardwareApi
from src.api.admin.smart_shelves_api import SmartShelvesApi
from src.resources.case import Case
from src.resources.activity import Activity
from src.bases.smart_shelves_basis import smart_shelves_basis
import time

def smart_shelf_move_locker_to_another_distributor(case):
    case.log_name(" Move Locker to another distributor and check shelves in planogram (SRX-8223) ")
    case.testrail_config(1969)

    try:
        lp = LoginPage(case.activity)
        ha = HardwareApi(case)
        ssa = SmartShelvesApi(case)
        ss = SmartShelvesPage(case.activity)

        # create smart shelf for main distributor
        response = smart_shelves_basis(case)
        locker_body = response["locker"]
        locker = locker_body["value"]
        iothub_body = response["iothub"]

        # create second smart shelf for main distributor
        response_second = smart_shelves_basis(case)
        locker_body_second = response_second["locker"]
        iothub_body_second = response_second["iothub"]

        # remove locker from smart shelf
        ssa.update_smart_shelf(locker_body=locker_body_second, locker_body_second=False)

        # create iot hub for second distributor
        iothub_response = ha.create_iothub(distributor_id=case.activity.variables.sub_distributor_id)

        lp.log_in_admin_portal()
        ss.sidebar_hardware()
        ss.check_smart_shelf_unavailable_via_planogram(locker, response["smart_shelf_number"], in_list=True)

        # move locker to iothub of second distributor
        first_locker_type_id = (ha.get_first_locker_type())["id"]
        ha.update_locker(locker_id=locker_body["id"], locker_type_id=first_locker_type_id, iothub_id=iothub_response["id"])

        ss.page_refresh()
        ss.wait_until_progress_bar_loaded()
        ss.sidebar_hardware()
        ss.check_smart_shelf_unavailable_via_planogram(locker, response_second["smart_shelf_number"])

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(locker_body["id"])
        ha.delete_hardware(locker_body_second["id"])
        time.sleep(5)
        ha.delete_hardware(iothub_body["id"])
        ha.delete_hardware(iothub_response["id"])
        ha.delete_hardware(iothub_body_second["id"])
        ssa.delete_smart_shelves(response["smart_shelves_id"])
        ssa.delete_smart_shelves(response_second["smart_shelves_id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    smart_shelf_move_locker_to_another_distributor(Case(Activity()))