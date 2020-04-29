from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.testrail import Testrail
from src.cases.ui import *
from src.cases.smoke import *
import traceback

if __name__ == "__main__":
    #smoke tests
    try:
        #test cases
        smoke_ui_suite = [
            customer_login,
            checkout_login,
        ]

        smoke_api_suite = [
            get_settings,
            create_user,
            label_transaction_activity_log,
            import_product
        ]
        
        #UI part
        activity = Activity(smoke=True)

        try:
            distributor_token = distributor_login(Case(activity))
        except:
            activity.logger.error(f"Error with the distributor login test case. Authorization token was not received", True)

        for test_case in smoke_ui_suite:
            try:
                case = Case(activity)
                test_case(case)
            except:
                activity.logger.error(f"Error with test case '{str(test_case)}'", True)

        try:
            activity.logger.my_logger.handlers.clear()
        except:
            pass

        #API part
        api_activity = Activity(api_test=True, smoke=True)

        for test_case in smoke_api_suite:
            try:
                case = Case(api_activity)
                case.distributor_token = distributor_token
                test_case(case)
            except:
                activity.logger.error(f"Error with test case '{str(test_case)}'", True)

        testrail = Testrail(activity.testrail_email, activity.testrail_password)
        tests = testrail.get_tests(activity.variables.run_number[0])
        for test in tests:
            if (test["status_id"] == 5):
                activity.logger.info("There are failed tests")
                testrail.run_report(activity.variables.report_id)
                break
        else:
            activity.logger.info("All test are passed")

    except:
        print(str(traceback.format_exc()))

