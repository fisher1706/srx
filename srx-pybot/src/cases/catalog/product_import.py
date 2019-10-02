from src.pages.sub.login_page import LoginPage
from src.pages.distributor.catalog_page import CatalogPage
from src.resources.case import Case
from src.resources.activity import Activity

def product_import(case):
    case.log_name("Product import")
    case.testrail_config(case.activity.variables.run_number, 34)

    try:
        lp = LoginPage(case.activity)
        cp = CatalogPage(case.activity)
        product_body = cp.product_body.copy()

        #-------------------
        product_body["partSku"] = case.random_string_u(18)
        product_body["shortDescription"] = product_body["partSku"]+" - short description"
        product_body["roundBuy"] = "39"
        #-------------------
        products = [
            [product_body["partSku"], None, None, product_body["shortDescription"], None, None, None, None, None, None, None, None, None, product_body["roundBuy"], None, None, None, None, None, None, None, None, None, None]
        ]
        lp.log_in_distributor_portal()
        cp.sidebar_catalog()
        cp.import_product(products)
        cp.check_last_product(product_body.copy())

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    product_import(Case(Activity()))