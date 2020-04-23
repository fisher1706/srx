from src.resources.case import Case
from src.resources.activity import Activity
from src.api.distributor.settings_api import SettingsApi

def get_settings(case):
    case.log_name("Get shipto settings")
    case.testrail_config(2001)

    try:
        sa = SettingsApi(case)

        sa.get_checkout_software_settings_for_shipto(case.activity.variables.shipto_id)

        case.finish_case()
    except:
        case.critical_finish_case()
    
if __name__ == "__main__":
    case = Case(Activity(api_test=True, smoke=True))
    distributor_token = SettingsApi(case).get_distributor_token()
    get_settings(case)