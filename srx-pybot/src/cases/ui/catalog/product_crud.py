from src.pages.sub.login_page import LoginPage
from src.pages.distributor.catalog_page import CatalogPage
from src.resources.case import Case
from src.resources.activity import Activity

def product_crud(case):
    case.log_name("Product CRUD")
    case.testrail_config(case.activity.variables.run_number, 33)

    try:
        lp = LoginPage(case.activity)
        cp = CatalogPage(case.activity)
        product_body = cp.product_body.copy()
        edit_product_body = cp.product_body.copy()

        #-------------------
        product_body["partSku"] = case.random_string_u(18)
        product_body["shortDescription"] = f"{product_body['partSku']} - short description"
        product_body["roundBuy"] = "15"
        #-------------------
        edit_product_body["partSku"] = case.random_string_u(18)
        edit_product_body["shortDescription"] = f"{product_body['partSku']} - edit short description"
        edit_product_body["roundBuy"] = "27"
        edit_product_body["lifecycleStatus"] = "OBSOLETE"
        edit_product_body["image"] = "example.com"
        edit_product_body["longDescription"] = "long description"
        edit_product_body["weight"] = "100"
        edit_product_body["height"] = "200"
        edit_product_body["width"] = "300"
        edit_product_body["length"] = "400"
        edit_product_body["issueQuantity"] = "500"
        edit_product_body["packageConversion"] = "600"
        edit_product_body["manufacturerPartNumber"] = "700"
        edit_product_body["manufacturer"] = "800"
        edit_product_body["alternative"] = "900"
        edit_product_body["productLvl1"] = "1000"
        edit_product_body["productLvl2"] = "1100"
        edit_product_body["productLvl3"] = "1200"
        edit_product_body["attribute1"] = "1300"
        edit_product_body["attribute2"] = "1400"
        edit_product_body["attribute3"] = "1500"
        edit_product_body["gtin"] = "1600"
        edit_product_body["upc"] = "1700"
        edit_product_body["keyword"] = "1800"
        edit_product_body["unitName"] = "1900"
        #-------------------

        lp.log_in_distributor_portal()
        cp.sidebar_catalog()
        cp.create_product(product_body.copy())
        cp.check_last_product(product_body.copy())
        cp.update_last_product(edit_product_body.copy())
        cp.check_last_product(edit_product_body.copy())

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    product_crud(Case(Activity()))