from src.pages.sub.login_page import LoginPage
from src.pages.admin.universal_catalog_page import UniversalCatalogPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def universal_catalog_crud(case):
    case.log_name("Universal catalog CRUD")
    case.testrail_config(1857)

    try:
        lp = LoginPage(case.activity)
        ucp = UniversalCatalogPage(case.activity)
        universal_product_body = ucp.universal_product_body.copy()
        edit_universal_product_body = ucp.universal_product_body.copy()

        #-------------------
        universal_product_body["upc"] = Tools.random_string_u(18)
        universal_product_body["manufacturerPartNumber"] = Tools.random_string_u(18)
        #-------------------
        edit_universal_product_body["manufacturerPartNumber"] = Tools.random_string_u(18)
        edit_universal_product_body["manufacturer"] = Tools.random_string_u(18)
        edit_universal_product_body["gtin"] = Tools.random_string_u(18)
        edit_universal_product_body["upc"] = Tools.random_string_u(18)
        #-------------------
        table_body = ucp.remapping_to_table_keys(universal_product_body.copy())
        edit_table_body = ucp.remapping_to_table_keys(edit_universal_product_body.copy())

        lp.log_in_admin_portal()
        ucp.sidebar_universal_catalog()
        ucp.create_universal_product(universal_product_body.copy())
        new_product_row = ucp.scan_table(universal_product_body["upc"], "UPC", table_body.copy())
        ucp.update_universal_product(edit_universal_product_body.copy(), new_product_row)
        new_product_row = ucp.scan_table(edit_universal_product_body["upc"], "UPC", edit_table_body.copy())
        ucp.delete_universal_product(new_product_row)

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    universal_catalog_crud(Case(Activity()))