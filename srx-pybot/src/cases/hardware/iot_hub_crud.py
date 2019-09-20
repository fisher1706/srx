from src.pages.sub.login_page import LoginPage
from src.pages.admin.hardware_page import HardwarePage
from src.resources.case import Case
from src.resources.activity import Activity
import time

def iot_hub_crud(case):
    case.log_name("IoT Hub CRUD")
    case.testrail_config(case.activity.variables.run_number, 32)

    try:
        lp = LoginPage(case.activity)
        hp = HardwarePage(case.activity)

        lp.log_in_admin_portal()
        hp.sidebar_hardware()
        serial_number = hp.create_iot_hub(case.activity.variables.distributor_name)
        hp.check_last_hardware(serial_number=serial_number, device_type="IOTHUB", distributor=case.activity.variables.distributor_name)
        hp.update_last_iot_hub(case.activity.variables.sub_distributor_name)
        hp.check_last_hardware(serial_number=serial_number, device_type="IOTHUB", distributor=case.activity.variables.sub_distributor_name)
        hp.remove_last_hardware()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    iot_hub_crud(Case(Activity()))