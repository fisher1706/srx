from src.pages.sub.login_page import LoginPage
from src.pages.distributor.warehouses_page import WarehousesPage
from src.resources.case import Case
from src.resources.activity import Activity

def warehouses_crud(case):
    case.log_name("Warehouses CRUD")
    #case.testrail_config(case.activity.variables.run_number, 28)
    lp = LoginPage(case.activity)
    wp = WarehousesPage(case.activity)

    lp.log_in_distributor_portal()
    wp.sidebar_warehouses()
    wp.create_warehouse(name, number, address1, address2, city, state, code, timezone, contact_email, invoice_email)
    wp.check_last_warehouse(name, number, timezone, address, contact_email, invoice_email)
    wp.update_warehouse(name, number, address1, address2, city, state, code, timezone, contact_email, invoice_email)
    wp.check_last_warehouse(name, number, timezone, address, contact_email, invoice_email)
    wp.delete_last_warehouse()
    case.finish_case()

if __name__ == "__main__":
    distributor_users_crud(Case(Activity()))