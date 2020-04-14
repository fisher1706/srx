from src.pages.sub.login_page import LoginPage
from src.pages.distributor.pricing_page import PricingPage
from src.resources.case import Case
from src.resources.activity import Activity
import random

def pricing_import(case):
    case.log_name("Pricing import")
    case.testrail_config(35)

    try:
        lp = LoginPage(case.activity)
        pp = PricingPage(case.activity)
        pricing_body = pp.pricing_body.copy()
        temporary_price = str(random.choice(range(100)))

        #-------------------
        pricing_body["SKU"] = "PRICING_SKU"
        pricing_body["Price"] = "$"+temporary_price+".00"
        pricing_body["UOM"] = "M"
        pricing_body["Expiration Date"] = "Fri, Dec 12, 2025"
        #-------------------
        pricing = [
            [pricing_body["SKU"], temporary_price, pricing_body["UOM"], "12/12/2025 10:15:30"]
        ]
        #-------------------

        lp.log_in_distributor_portal()
        pp.sidebar_pricing()
        pp.select_customer_shipto(customer_name=case.activity.variables.customer_name)
        pp.import_pricing(pricing)
        pp.select_customer_shipto(customer_name=case.activity.variables.customer_name)
        pp.check_price_by_name(pricing_body.copy())

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    pricing_import(Case(Activity()))