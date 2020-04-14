from src.pages.sub.login_page import LoginPage
from src.pages.admin.admin_portal_page import AdminPortalPage
from src.pages.admin.fees_page import FeesPage
from src.resources.case import Case
from src.resources.activity import Activity
import random

def shipto_fee_levels(case):
    case.log_name("Shipto levels undo")
    case.testrail_config(1919)

    try:
        lp = LoginPage(case.activity)
        fp = FeesPage(case.activity)
        fee_price = fp.fee_price.copy()
        edit_fee_price = fp.fee_price.copy()

        #-------------------
        fee_price["Level 1"] = random.randint(10, 100)
        fee_price["Level 2"] = random.randint(10, 100)
        fee_price["Level 3"] = random.randint(10, 100)

        #-------------------
        edit_fee_price["Level 1"] = random.randint(10, 100)
        edit_fee_price["Level 2"] = random.randint(10, 100)
        edit_fee_price["Level 3"] = random.randint(10, 100)

        lp.log_in_admin_portal()
        fp.sidebar_fees()
        fp.set_fee_price(fee_price.copy())
        fp.check_fee_price(fee_price.copy())
        fp.set_fee_price(edit_fee_price.copy())
        fp.undo(edit_fee_price.copy())
        fp.check_fee_price(fee_price.copy())
        case.finish_case()

    except:
        case.critical_finish_case()

if __name__ == "__main__":
    shipto_fee_levels(Case(Activity()))
