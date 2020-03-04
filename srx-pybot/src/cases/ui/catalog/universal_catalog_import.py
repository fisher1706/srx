from src.pages.sub.login_page import LoginPage
from src.pages.admin.universal_catalog_page import UniversalCatalogPage
from src.resources.case import Case
from src.resources.activity import Activity
from src.resources.tools import Tools

def universal_catalog_import(case):
    case.log_name("Universal catalog import")
    case.testrail_config(case.activity.variables.run_number, 1858)

    try:
        lp = LoginPage(case.activity)
        ucp = UniversalCatalogPage(case.activity)
        universal_product_body = ucp.universal_product_body.copy()

        #-------------------
        universal_product_body["manufacturerPartNumber"] = Tools.random_string_u(18)
        universal_product_body["manufacturer"] = Tools.random_string_u(18)
        universal_product_body["gtin"] = Tools.random_string_u(18)
        universal_product_body["upc"] = Tools.random_string_u(18)
        #-------------------
        table_body = ucp.remapping_to_table_keys(universal_product_body.copy())

        universal_catalog_import = [
            [universal_product_body["upc"], universal_product_body["gtin"], universal_product_body["manufacturer"], universal_product_body["manufacturerPartNumber"]]
        ]

        lp.log_in_admin_portal()
        ucp.sidebar_universal_catalog()
        ucp.import_universal_catalog(universal_catalog_import)
        new_product_row = ucp.scan_table(universal_product_body["upc"], "UPC", table_body.copy())
        ucp.delete_universal_product(new_product_row)

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    universal_catalog_import(Case(Activity()))