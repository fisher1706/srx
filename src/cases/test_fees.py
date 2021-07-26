import pytest
import random
from src.pages.general.login_page import LoginPage
from src.pages.admin.fees_page import FeesPage

@pytest.mark.regression
def test_shipto_fee_levels(ui):
    ui.testrail_case_id = 1919

    lp = LoginPage(ui)
    fp = FeesPage(ui)
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