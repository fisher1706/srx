from src.pages.sub.login_page import LoginPage
from src.pages.admin.hardware_page import HardwarePage
from src.api.admin.hardware_api import HardwareApi
from src.resources.case import Case
from src.resources.activity import Activity

def common_set_of_hubs_for_locker_and_vending(case):
    case.log_name("Common set of available IoT Hubs for Lockers and Vending Machines")
    case.testrail_config(case.activity.variables.run_number, 1839)

    try:
        lp = LoginPage(case.activity)
        hp = HardwarePage(case.activity)
        ha = HardwareApi(case)

        lp.log_in_admin_portal()

        iothub_dto = ha.create_iothub() #create IoT Hub via rest api
        iothub_name = str(iothub_dto["id"]) +" ("+iothub_dto["value"]+")"
        
        hp.sidebar_hardware()
        hp.wait_until_page_loaded()
        hp.iothub_should_be_available("Locker", iothub_name)
        hp.iothub_should_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        locker_serial_number = hp.create_locker(case.activity.variables.distributor_name, iothub_name) #create locker
        hp.check_last_hardware(device_type="Locker", distributor=case.activity.variables.distributor_name)

        hp.iothub_should_not_be_available("Locker", iothub_name)
        hp.iothub_should_not_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        hp.remove_last_hardware("LOCKER") #remove locker

        hp.iothub_should_be_available("Locker", iothub_name)
        hp.iothub_should_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        locker_serial_number = hp.create_vending(case.activity.variables.distributor_name, iothub_name) #create vending
        hp.check_last_hardware(device_type="Vending", distributor=case.activity.variables.distributor_name)

        hp.iothub_should_not_be_available("Locker", iothub_name)
        hp.iothub_should_not_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        hp.remove_last_hardware("VENDING") #remove vending

        hp.iothub_should_be_available("Locker", iothub_name)
        hp.iothub_should_be_available("Vending", iothub_name)
        hp.iothub_should_be_available("IP Camera", iothub_name)

        case.finish_case()
    except:
        case.critical_finish_case()

    try:
        ha.delete_hardware(iothub_dto["id"])
    except:
        case.print_traceback()

if __name__ == "__main__":
    common_set_of_hubs_for_locker_and_vending(Case(Activity()))