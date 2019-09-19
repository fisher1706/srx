from src.pages.sub.login_page import LoginPage
from src.pages.distributor.customers_page import CustomersPage
from src.resources.case import Case
from src.resources.activity import Activity

def customer_crud(case):
    case.log_name("Customer CRUD")
    case.testrail_config(case.activity.variables.run_number, 31)

    try:
        lp = LoginPage(case.activity)
        cp = CustomersPage(case.activity)

        #-------------------
        name = "Customer Name"
        number = ""
        customer_type = "Test Customer"
        market_type = "Not specified"
        warehouse_name = "A_Warehouse"
        warehouse_number = "1138"
        notes = ""
        supply_force = "false"
        #-------------------
        edit_name = "Customer Edit Name"
        edit_number = "Customer Edit Number"
        edit_customer_type = "Not specified"
        edit_market_type = "Not specified"
        edit_warehouse = "Z_Warehouse (9999)"
        edit_notes = "any note"
        edit_supply_force = "true"
        #-------------------

        lp.log_in_distributor_portal()
        cp.sidebar_customers()
        cp.create_customer(name=name, number=number, customer_type=customer_type, market_type=market_type, warehouse=warehouse_name+" ("+warehouse_number+")", notes=notes, supply_force=supply_force)
        cp.check_last_customer(name=name, number=number, customer_type=customer_type, market_type=market_type, warehouse=warehouse_name+"("+warehouse_number+")")
        cp.update_customer(name=edit_name, number=edit_number, customer_type=edit_customer_type, market_type=edit_market_type, notes=edit_notes, supply_force=edit_supply_force)
        cp.sidebar_customers()
        cp.check_last_customer(name=edit_name, number=edit_number, customer_type=edit_customer_type, market_type=edit_market_type, warehouse=warehouse_name+"("+warehouse_number+")")
        cp.delete_last_customer()
        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    customer_crud(Case(Activity()))