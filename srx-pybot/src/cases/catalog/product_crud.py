from src.pages.sub.login_page import LoginPage
from src.pages.distributor.catalog_page import CatalogPage
from src.resources.case import Case
from src.resources.activity import Activity
import time as t

def product_crud(case):
    case.log_name("Product CRUD")
    #case.testrail_config(case.activity.variables.run_number, 29)

    try:
        lp = LoginPage(case.activity)
        cp = CatalogPage(case.activity)

        #-------------------
        sku = case.random_string_u(18)
        short_description = sku+" - short description"
        round_buy = "15"
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
        cp.sidebar_catalog()
        cp.create_product(sku=sku, short_description=short_description, round_buy=round_buy)
        #t.sleep(7)
        cp.check_last_product(sku=sku, short_description=short_description, round_buy=round_buy)
        #p.update_last_product(name=edit_name, number=edit_number, address1=edit_address1, address2=edit_address2, city=edit_city, state=edit_state, code=edit_code, timezone=edit_timezone, contact_email=edit_contact_email, invoice_email=edit_invoice_email)
        #cp.check_last_product(name=edit_name, number=edit_number, timezone=edit_timezone, address=[edit_address1, edit_address1, edit_city, edit_short_state, edit_code], contact_email=edit_contact_email, invoice_email=edit_invoice_email)
        #cp.delete_last_product()
        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    product_crud(Case(Activity()))