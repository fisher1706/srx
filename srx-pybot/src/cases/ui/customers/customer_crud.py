from src.pages.sub.login_page import LoginPage
from src.pages.distributor.customers_page import CustomersPage
from src.resources.case import Case
from src.resources.activity import Activity

def customer_crud(case):
    case.log_name("Customer CRUD")
    case.testrail_config(31)

    try:
        lp = LoginPage(case.activity)
        cp = CustomersPage(case.activity)
        customer_body = cp.customer_body.copy()
        edit_customer_body = cp.customer_body.copy()

        #-------------------
        customer_body["name"] = "Customer Name"
        customer_body["customerType"] = "Test Customer"
        customer_body["marketType"] = "Not specified"
        customer_body["warehouse"] = "A_Warehouse (1138)"
        #-------------------
        edit_customer_body["name"] = "Customer Edit Name"
        edit_customer_body["number"] = "Customer Edit Number"
        edit_customer_body["customerType"] = "Not specified"
        edit_customer_body["marketType"] = "Not specified"
        edit_customer_body["notes"] = "any note"
        edit_customer_body["supplyForce"] = "true"
        #-------------------

        lp.log_in_distributor_portal()
        cp.sidebar_customers()
        cp.create_customer(customer_body.copy())
        cp.check_last_customer(customer_body.copy())
        cp.update_last_customer(edit_customer_body.copy())
        cp.sidebar_customers()
        cp.check_last_customer(edit_customer_body.copy())
        cp.delete_last_customer()

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    customer_crud(Case(Activity()))