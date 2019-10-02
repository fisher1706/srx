from src.pages.sub.login_page import LoginPage
from src.pages.distributor.pricing_page import PricingPage
from src.resources.case import Case
from src.resources.activity import Activity
import random

def pricing_import(case):
    case.log_name("Pricing import")
    #case.testrail_config(case.activity.variables.run_number, 34)

    try:
        lp = LoginPage(case.activity)
        pp = PricingPage(case.activity)
        pricing_body = pp.pricing_body.copy()

        #-------------------
        pricing_body["SKU"] = "PRICING_SKU"
        pricing_body["Price"] = str(random.choice(range(10000))/100)
        pricing_body["UOM"] = "M"
        pricing_body["Expiration Date"] = "12/12/2025 10:15:30"
        #-------------------

        pricing = [
            [pricing_body["SKU"], pricing_body["Price"], pricing_body["UOM"], pricing_body["Expiration Date"]]
        ]

        lp.log_in_distributor_portal()
        pp.sidebar_pricing()
        pp.select_customer_shipto()
        pp.import_pricing(pricing)
        pp.check_price_by_name(pricing_body.copy())

        case.finish_case()
    except:
        case.critical_finish_case()

if __name__ == "__main__":
    pricing_import(Case(Activity()))