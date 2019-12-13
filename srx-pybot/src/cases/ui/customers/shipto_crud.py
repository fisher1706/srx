from src.pages.sub.login_page import LoginPage
from src.pages.distributor.shipto_page import ShiptoPage
from src.resources.case import Case
from src.resources.activity import Activity

def shipto_crud(case):
    case.log_name("ShipTo CRUD")
    case.testrail_config(case.activity.variables.run_number, 241)

    try:
        lp = LoginPage(case.activity)
        sp = ShiptoPage(case.activity)
        shipto_body = sp.shipto_body.copy()
        edit_shipto_body = sp.shipto_body.copy()

        #-------------------
        shipto_body["number"] = case.random_string_l(12)
        shipto_body["poNumber"] = case.random_string_l(10)
        shipto_body["address.zipCode"] = "77777"
        shipto_body["address.line1"] = "test_address 1"
        shipto_body["address.city"] = "test city)"
        shipto_body["state"] = "Alaska"
        #-------------------
        edit_shipto_body["number"] = case.random_string_l(12)
        edit_shipto_body["name"] = case.random_string_l(10)
        edit_shipto_body["poNumber"] = case.random_string_l(10)
        edit_shipto_body["address.zipCode"] = "77777"
        edit_shipto_body["address.line1"] = "test_address 1"
        edit_shipto_body["address.line2"] = "test_address 2"
        edit_shipto_body["address.city"] = "test city)"
        edit_shipto_body["state"] = "Alaska"
        edit_shipto_body["notes"] = "some notes"
        edit_shipto_body["contactId"] = "11111"
        #-------------------

        lp.log_in_distributor_portal()
        sp.follow_shipto_url()
        sp.create_shipto(shipto_body.copy())
        sp.check_last_shipto(shipto_body.copy())
        sp.update_last_shipto(edit_shipto_body.copy())
        sp.follow_shipto_url()
        sp.check_last_shipto(edit_shipto_body.copy())
        sp.delete_last_shipto()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    shipto_crud(Case(Activity()))