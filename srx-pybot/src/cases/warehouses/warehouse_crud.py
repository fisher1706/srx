from src.pages.sub.login_page import LoginPage
from src.pages.distributor.warehouses_page import WarehousesPage
from src.resources.case import Case
from src.resources.activity import Activity

def warehouse_crud(case):
    case.log_name("Warehouse CRUD")
    case.testrail_config(case.activity.variables.run_number, 29)

    try:
        lp = LoginPage(case.activity)
        wp = WarehousesPage(case.activity)

        #-------------------
        name = "Warehouse Name"
        number = "Warehouse Number"
        address1 = "Warehouse Address 1"
        address2 = ""
        city = "Warehouse City"
        state = "Georgia"
        short_state = "GA"
        code = "33333"
        timezone = "America/Halifax (-03:00)"
        contact_email = case.random_email()
        invoice_email = case.random_email()
        #-------------------
        edit_name = "Warehouse Edit Name"
        edit_number = "Warehouse Edit Number"
        edit_address1 = "Warehouse Edit Address 1"
        edit_address2 = "Warehouse Edit Address 2"
        edit_city = "Warehouse Edit City"
        edit_state = "Colorado"
        edit_short_state = "CO"
        edit_code = "99999"
        edit_timezone = "America/Atka (-09:00)"
        edit_contact_email = case.random_email()
        edit_invoice_email = case.random_email()
        #-------------------

        lp.log_in_distributor_portal()
        wp.sidebar_warehouses()
        wp.create_warehouse(name=name, number=number, address1=address1, address2=address2, city=city, state=state, code=code, timezone=timezone, contact_email=contact_email, invoice_email=invoice_email)
        wp.check_last_warehouse(name=name, number=number, timezone=timezone, address=[address1, city, short_state, code], contact_email=contact_email, invoice_email=invoice_email)
        wp.update_warehouse(name=edit_name, number=edit_number, address1=edit_address1, address2=edit_address2, city=edit_city, state=edit_state, code=edit_code, timezone=edit_timezone, contact_email=edit_contact_email, invoice_email=edit_invoice_email)
        wp.check_last_warehouse(name=edit_name, number=edit_number, timezone=edit_timezone, address=[edit_address1, edit_address1, edit_city, edit_short_state, edit_code], contact_email=edit_contact_email, invoice_email=edit_invoice_email)
        wp.delete_last_warehouse()
        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    warehouse_crud(Case(Activity()))