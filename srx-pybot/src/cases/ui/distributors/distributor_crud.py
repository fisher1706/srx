from src.pages.sub.login_page import LoginPage
from src.pages.admin.distributor_admin_page import DistributorAdminPage
from src.pages.admin.admin_portal_page import AdminPortalPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools
import time

def distributor_crud(case):
    case.log_name("Distributor CRUD")
    case.testrail_config(1917)

    try:
        lp = LoginPage(case.activity)
        dp = DistributorAdminPage(case.activity)
        distributor_body = dp.distributor_body.copy()
        edit_distributor_body = dp.distributor_body.copy()
        table_cells_checkbox = dp.table_cells_checkbox.copy()
        edit_table_cells_checkbox = dp.table_cells_checkbox.copy()

        #-------------------
        distributor_body["name"] = "my First"
        distributor_body["invoiceEmail"] = Tools.random_email()
        distributor_body["address.line1"] = "my adress line 1"
        distributor_body["address.line2"] = "my adress line 2"
        distributor_body["address.city"] = "Boston"
        distributor_body["address.zipCode"] = "02101"
        distributor_body["billingDelay"] = "3"
        state = "Massachusetts"
        bill_by = "SKU"
        checkbox_list = ["Processing Fee", "Supply Force", "User Data", "Agreements", "Billing Info"]

        #-------------------
        edit_distributor_body["name"] = "my Edit First"
        edit_distributor_body["invoiceEmail"] = Tools.random_email()
        edit_distributor_body["address.line1"] = "my Edit adress line 1"
        edit_distributor_body["address.line2"] = "my Edit adress line 2"
        edit_distributor_body["address.city"] = "Fairbanks"
        edit_distributor_body["address.zipCode"] = "99703"
        edit_distributor_body["billingDelay"] = "5"
        edit_checkbox_list = ["Processing Fee", "Supply Force"]
        edit_state = "Alaska"
        edit_bill_by = "ShipTo"
        ship_to_level = "Level 1"
        edit_table_cells_checkbox["Process.Fee"] = False
        edit_table_cells_checkbox["SupplyForce"] = False
        #-------------------

        lp.log_in_admin_portal()
        dp.sidebar_distributors()
        time.sleep(7)
        check_mark = dp.create_distributor(distributor_body.copy(), state=state, bill_by=bill_by, checkbox_list=checkbox_list)
        dp.check_last_distributor(distributor_body.copy(), state_short_code="MA", table_cells_checkbox=table_cells_checkbox, check_mark=check_mark)
        dp.update_last_distributor(edit_distributor_body.copy(), state=edit_state, bill_by=edit_bill_by, checkbox_list=edit_checkbox_list, ship_to_level=ship_to_level)
        dp.check_last_distributor(edit_distributor_body.copy(), "AK", table_cells_checkbox=edit_table_cells_checkbox, check_mark=check_mark)
        dp.delete_last_distributor()
        case.finish_case()

    except:
        case.critical_finish_case()

if __name__ == "__main__":
    distributor_crud(Case(Activity()))
