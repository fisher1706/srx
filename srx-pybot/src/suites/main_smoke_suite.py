from src.resources.case import Case
from src.resources.activity import Activity
from src.cases.ui import *
from src.cases.smoke import *
import traceback

if __name__ == "__main__":
    #smoke tests
    try:
        activity = Activity(smoke=True)
        
        try:
            distributor_token = distributor_login(Case(activity))
        except:
            pass

        smoke_ui_suite = [
            customer_login,
            checkout_login,
        ]

        smoke_api_suite = [
            get_settings,
            create_user,
            create_user,
            label_transaction_activity_log
        ]

        for test_case in smoke_ui_suite:
            try:
                test_case(Case(activity))
            except:
                pass

        activity.logger.my_logger.handlers.clear()
        api_activity = Activity(api_test=True, smoke=True)

        for test_case in smoke_api_suite:
            try:
                case = Case(api_activity)
                case.distributor_token = distributor_token
                test_case(Case(api_activity))
            except:
                pass

    except:
        print(str(traceback.format_exc()))

