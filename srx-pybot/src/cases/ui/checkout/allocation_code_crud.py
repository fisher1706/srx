from src.pages.sub.login_page import LoginPage
from src.pages.customer.allocation_codes_page import AllocationCodesPage
from src.pages.sub.activity_log_page import ActivityLogPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools
import time

def allocation_code_crud(case):
    case.log_name("Allocation code CRUD")
    case.testrail_config(case.activity.variables.run_number, 42)

    try:
        lp = LoginPage(case.activity)
        acp = AllocationCodesPage(case.activity)
        alp = ActivityLogPage(case.activity)
        allocation_code_body = acp.allocation_code_body.copy()
        edit_allocation_code_body = acp.allocation_code_body.copy()

        #-------------------
        allocation_code_body["name"] = Tools.random_string_u(10)
        allocation_code_body["type"] = "Dropdown"
        allocation_code_body["values"] = [Tools.random_string_u(7), Tools.random_string_u(7)]
        allocation_code_body["isRequired"] = True
        allocation_code_body["shiptos"] = [case.activity.variables.shipto_number]
        #-------------------
        edit_allocation_code_body["name"] = Tools.random_string_u(10)
        edit_allocation_code_body["values"] = [Tools.random_string_u(7)]
        edit_allocation_code_body["isRequired"] = False
        #-------------------
        activity_log_main_body = {
            "Type": "AllocationCodes",
            "Action": "ALLOCATION_CODES_CREATE",
            "User": case.activity.variables.customer_email,
            "User Type": "USER",
            "Result": "SUCCESS"
        }
        #-------------------
        activity_log_expanded_body = {
            "codeType": "DROP_DOWN",
            "name": allocation_code_body["name"]
        }
        #-------------------

        lp.log_in_customer_portal()
        acp.sidebar_allocation_codes()
        acp.add_allocation_code(allocation_code_body.copy())
        acp.check_allocation_code(allocation_code_body.copy())
        acp.sidebar_activity_feed()
        acp.page_refresh()
        alp.check_last_activity_log(activity_log_main_body.copy(), activity_log_expanded_body.copy())

        acp.sidebar_allocation_codes()
        acp.update_allocation_code(allocation_code_body["name"], edit_allocation_code_body.copy())

        acp.sidebar_activity_feed()
        acp.page_refresh()
        activity_log_main_body["Action"] = "ALLOCATION_CODES_UPDATE"
        activity_log_expanded_body["name"] = edit_allocation_code_body["name"]
        alp.check_last_activity_log(activity_log_main_body.copy(), activity_log_expanded_body.copy())

        acp.sidebar_allocation_codes()
        acp.wait_until_page_loaded()
        acp.check_allocation_code(edit_allocation_code_body.copy())
        acp.delete_allocation_code(edit_allocation_code_body["name"])

        acp.sidebar_activity_feed()
        acp.page_refresh()
        activity_log_main_body["Action"] = "ALLOCATION_CODES_DELETE"
        alp.check_last_activity_log(activity_log_main_body.copy(), activity_log_expanded_body.copy())

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    allocation_code_crud(Case(Activity()))