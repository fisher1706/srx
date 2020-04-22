from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.hardware_api import HardwareApi
from src.resources.tools import Tools

def create_user(case, token):
    case.log_name("Get device status")
    case.testrail_config(2003)

    try:
        ha = HardwareApi(case)
        response = ha.get_device_status()
        count = len(response)
        assert count != 0, "Device statuses list is empty"

        case.finish_case()
    except:
        case.critical_finish_case()
    
if __name__ == "__main__":
    case = Case(Activity(api_test=True, smoke=True))
    distributor_token = HardwareApi(case).get_distributor_token()
    create_user(case, distributor_token)